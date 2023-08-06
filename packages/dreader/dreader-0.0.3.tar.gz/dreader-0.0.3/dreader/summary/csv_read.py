import csv
from dataclasses import dataclass
from dreader.config_params import DipoleOrientation, StrainFieldType


@dataclass
class SummaryRow:
	"""
	Represents a row of a bayesrun probs summary file
	"""

	config_seed: int
	sample_index: int
	temperature: float
	orientation: DipoleOrientation
	pfixexp: float
	avg_filled: int
	total_slots: int
	strain_field_type: StrainFieldType
	strain_field: float
	cumulative_prob_from_zero_temp: float


def read_all_rows(file):
	"""
	Takes in a file handle, reads to rows with a dictreader.

	Basically a thin wrapper over csv.DictReader in case there's transformation we need here.
	"""
	reader = csv.DictReader(file)
	return [parse_row(row) for row in reader]


def parse_orientation(orientation_string: str) -> DipoleOrientation:
	return {
		"free": DipoleOrientation.FREE,
		"fixedxy": DipoleOrientation.FIXED_XY,
		"fixedz": DipoleOrientation.FIXED_Z,
	}[orientation_string]


def parse_strain_field_type(strain_field_type: str) -> StrainFieldType:
	return {
		"zeromean": StrainFieldType.ZERO_MEAN,
		"nonzeromean": StrainFieldType.NON_ZERO_MEAN,
	}[strain_field_type]


def parse_row(row):
	return SummaryRow(
		config_seed=int(row["config_seed"]),
		sample_index=int(row["sample_index"]),
		# don't think we actually need this
		# htcondor_subseed_count: int(row.htcondor_subseed_count),
		temperature=float(row["temperature"]),
		orientation=parse_orientation(row["orientation"]),
		pfixexp=float(row["pfixexp"]),
		avg_filled=int(row["avg_filled"]),
		total_slots=int(row["total_slots"]),
		strain_field_type=parse_strain_field_type(row["strain_field_type"]),
		strain_field=float(row["strain_field"]),
		# if we need these, here they are
		# monte_carlo_count: int(count),
		# monte_carlo_success: int(success),
		# likelihood: float(likelihood),
		cumulative_prob_from_zero_temp=float(row["cumulative_prob_from_zero_temp"]),
	)
