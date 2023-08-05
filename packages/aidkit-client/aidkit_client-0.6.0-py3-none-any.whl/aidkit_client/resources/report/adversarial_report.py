"""
Resources for the Adversarial Report.
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import altair as alt
from pandas import DataFrame

from aidkit_client._endpoints.models import (
    ModelNormStats,
    ReportAdversarialResponse,
    ReportRequest,
)
from aidkit_client._endpoints.report import ReportAPI
from aidkit_client.aidkit_api import HTTPService
from aidkit_client.configuration import get_api_client
from aidkit_client.resources.dataset import Dataset, Subset
from aidkit_client.resources.ml_model import MLModelVersion
from aidkit_client.resources.report._base_report import ModelComparisonView, _BaseReport


@dataclass
class AttackDetailView:
    """
    Attack-detail view of the report.
    """

    plot: alt.LayerChart


@dataclass
class AttackComparisonView:
    """
    Attack-comparison view of the report.
    """

    plot: alt.LayerChart
    stats: Dict[str, DataFrame]


class AdversarialReport(_BaseReport):
    """
    A report which compares model versions.
    """

    _data: ReportAdversarialResponse

    def __init__(
        self, api_service: HTTPService, report_response: ReportAdversarialResponse
    ) -> None:
        """
        Create a new instance from the server response.

        :param api_service: Service instance to use for communicating with the
            server.
        :param report_response: Server response describing the report
            to be created.
        """
        self._data = report_response
        self._api_service = api_service
        self.model = None

    @classmethod
    async def get(
        cls,
        model_id: int,
        model_versions: List[Union[int, MLModelVersion]],
        dataset: Union[int, Dataset],
        subset: Union[int, Subset],
        metrics: Optional[List[str]] = None,
        success_metric_threshold: float = 0.7,
    ) -> "AdversarialReport":
        """
        Get the adversarial report to compare the given model versions.

        :param model_id: ID of the uploaded model of which versions are compared in the report.
        :param model_versions: List of model versions to compare in the report.
        :param dataset: Dataset to use for the comparison.
        :param subset: Subset whose observations are used for the comparison.
        :param metrics: List of distance metrics to consider in the comparison.
        :param success_metric_threshold: Threshold used to convert
                                        a success metric score to a binary success criterion.
        :return: Instance of the adversarial report.
        """
        if metrics is None:
            metrics = []
        model_version_ids = [
            model_version.id if isinstance(model_version, MLModelVersion) else model_version
            for model_version in model_versions
        ]
        dataset_id = dataset.id if isinstance(dataset, Dataset) else dataset
        subset_id = subset.id if isinstance(subset, Subset) else subset
        api_service = get_api_client()
        report = AdversarialReport(
            api_service=api_service,
            report_response=await ReportAPI(api_service).get_adversarial_report(
                request=ReportRequest(
                    model=model_id,
                    model_versions=model_version_ids,
                    dataset=dataset_id,
                    subset=subset_id,
                    metrics=metrics,
                    success_metric_threshold=success_metric_threshold,
                )
            ),
        )
        report.model = model_id
        return report

    @staticmethod
    def _nested_dict_to_tuple_dict(
        nested_dict: Dict[str, Dict[str, Dict[str, ModelNormStats]]]
    ) -> Dict[Tuple[str, str, str], ModelNormStats]:
        return_dict: Dict[Tuple[str, str, str], ModelNormStats] = {}
        for index_1, dict_1 in nested_dict.items():
            for index_2, dict_2 in dict_1.items():
                for index_3, stats in dict_2.items():
                    return_dict[(index_1, index_2, index_3)] = stats
        return return_dict

    @classmethod
    def _get_model_comparison_stats(
        cls, stats_dict: Dict[str, Dict[str, Dict[str, Dict[str, ModelNormStats]]]]
    ) -> DataFrame:
        metrics_to_stat_mapper: Dict[Tuple[str, str, str, str], Dict[str, float]] = defaultdict(
            dict
        )
        for model_version, model_stats in stats_dict.items():
            for (
                distance_metric,
                success_metric,
                target_class,
            ), stats in cls._nested_dict_to_tuple_dict(model_stats).items():
                for stat_name, stat_value in stats:
                    metrics_to_stat_mapper[
                        (distance_metric, success_metric, target_class, stat_name)
                    ][model_version] = stat_value
        return DataFrame(metrics_to_stat_mapper)

    @classmethod
    def _get_attack_comparison_stats(
        cls,
        stats_dict: Dict[
            str, Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, ModelNormStats]]]]]
        ],
    ) -> Dict[str, DataFrame]:
        model_version_df_dict: Dict[str, DataFrame] = {}
        for model_version, attack_dict in stats_dict.items():
            stats_dict_in_pandas_form: Dict[
                Tuple[str, str, str, str], Dict[Tuple[str, str], float]
            ] = defaultdict(dict)
            for attack_class, attack_class_stats in attack_dict.items():
                for param_string, attack_instance_stats in attack_class_stats.items():
                    for (
                        distance_metric,
                        success_metric,
                        target_class,
                    ), stats in cls._nested_dict_to_tuple_dict(attack_instance_stats).items():
                        for stat_name, stat_value in stats.dict().items():
                            stats_dict_in_pandas_form[
                                (distance_metric, success_metric, target_class, stat_name)
                            ][(attack_class, param_string)] = stat_value
                        model_version_df_dict[model_version] = DataFrame(
                            data=stats_dict_in_pandas_form
                        )
        return model_version_df_dict

    def _fill_plot_with_data(self, plot: alt.LayerChart) -> alt.LayerChart:
        plot_copy = plot.copy(deep=True)
        plot_copy.data = self.data
        return plot_copy

    @property
    def model_comparison_view(self) -> ModelComparisonView:
        """
        Get the model-comparison view of the report.

        :return: Model-comparison view containing a plot and summary statistics.
        """
        return ModelComparisonView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.model_comparison_asr)
            ),
            stats=self._get_model_comparison_stats(self._data.stats.model_comparison_stats),
        )

    @property
    def attack_comparison_view(self) -> AttackComparisonView:
        """
        Get the attack-comparison view of the report.

        :return: Attack-comparison view containing a plot and summary statistics.
        """
        return AttackComparisonView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.attack_comparison_asr)
            ),
            stats=self._get_attack_comparison_stats(
                stats_dict=self._data.stats.attack_comparison_stats
            ),
        )

    @property
    def attack_detail_view(self) -> AttackDetailView:
        """
        Get the attack-detail view of the report.

        :return: Attack-detail view containing a plot.
        """
        return AttackDetailView(
            plot=self._fill_plot_with_data(
                alt.LayerChart.from_dict(self._data.plot_recipes.attack_detail_asr)
            )
        )
