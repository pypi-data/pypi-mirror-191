from typing import Callable, Union, Sequence, Tuple, TypeVar, Dict
from dreader.summary.csv_read import SummaryRow
from dreader.config_params import DipoleOrientation, StrainFieldType
from dataclasses import dataclass

A = TypeVar("A")


@dataclass
class SampleSummary:
	"""
	Represents a processed point for an entire sample, at a single temperature
	"""

	config_seed: int
	sample_index: int
	temperature: float
	ev_avg_filled: float
	ev_magnitude: float
	ev_strain_field_size: float
	preferred_orientation: DipoleOrientation
	preferred_orientation_confidence: float
	preferred_strain_field_type: StrainFieldType
	preferred_strain_field_type_confidence: float


def get_expectation_value(
	table: Sequence[SummaryRow], data_func: Callable[[SummaryRow], Union[int, float]]
) -> float:
	"""
	expectation value with no filtering
	"""
	total_prob = sum(r.cumulative_prob_from_zero_temp for r in table)
	return (
		sum([r.cumulative_prob_from_zero_temp * data_func(r) for r in table])
		/ total_prob
	)


def get_most_probable_and_confidence(
	table: Sequence[SummaryRow], data_func: Callable[[SummaryRow], A]
) -> Tuple[A, float]:
	cumulative_probs: Dict[A, float] = {}
	for row in table:
		val = data_func(row)
		if val in cumulative_probs:
			cumulative_probs[val] += row.cumulative_prob_from_zero_temp
		else:
			cumulative_probs[val] = row.cumulative_prob_from_zero_temp
	max_key = max(cumulative_probs, key=lambda x: cumulative_probs[x])
	return (max_key, cumulative_probs[max_key])


def max_temperature(table: Sequence[SummaryRow]) -> float:
	return max(table, key=lambda r: r.temperature).temperature


def get_sample_summary_from_filtered_table(
	filtered_table: Sequence[SummaryRow],
) -> SampleSummary:
	"""
	Needs filtered table with single config_seed, sample_index and temperature
	"""
	temperatures = set([r.temperature for r in filtered_table])
	if len(temperatures) != 1:
		raise ValueError(f"Did not have unique temperatures, got {temperatures}")

	config_seeds = set([r.config_seed for r in filtered_table])
	if len(config_seeds) != 1:
		raise ValueError(f"Did not have unique config_seeds, got {config_seeds}")

	sample_indexes = set([r.sample_index for r in filtered_table])
	if len(sample_indexes) != 1:
		raise ValueError(f"Did not have unique temperatures, got {sample_indexes}")

	# now we know they're unique

	preferred_orientation, orientation_confidence = get_most_probable_and_confidence(
		filtered_table, lambda r: r.orientation
	)
	preferred_strain_type, strain_type_confidence = get_most_probable_and_confidence(
		filtered_table, lambda r: r.strain_field_type
	)
	return SampleSummary(
		config_seed=config_seeds.pop(),
		sample_index=sample_indexes.pop(),
		temperature=temperatures.pop(),
		ev_avg_filled=get_expectation_value(filtered_table, lambda r: r.avg_filled),
		ev_magnitude=get_expectation_value(filtered_table, lambda r: r.pfixexp),
		ev_strain_field_size=get_expectation_value(
			filtered_table, lambda r: r.strain_field
		),
		preferred_orientation=preferred_orientation,
		preferred_orientation_confidence=orientation_confidence,
		preferred_strain_field_type=preferred_strain_type,
		preferred_strain_field_type_confidence=strain_type_confidence,
	)


def get_stats_for_table(table: Sequence[SummaryRow]) -> Sequence[SampleSummary]:
	max_temp = max_temperature(table)
	results = []
	sample_indexes = sorted(list(set([r.sample_index for r in table])))
	results = [
		get_sample_summary_from_filtered_table(
			[
				row
				for row in table
				if row.temperature == max_temp and row.sample_index == current_sample
			]
		)
		for current_sample in sample_indexes
	]
	return results
