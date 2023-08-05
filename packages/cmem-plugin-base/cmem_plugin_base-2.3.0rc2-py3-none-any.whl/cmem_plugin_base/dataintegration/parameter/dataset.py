"""DI Dataset Parameter Type."""
from typing import Optional

from cmem.cmempy.workspace.search import list_items
from cmem.cmempy.workspace.tasks import get_task

from cmem_plugin_base.dataintegration.context import PluginContext
from cmem_plugin_base.dataintegration.types import StringParameterType, Autocompletion
from cmem_plugin_base.dataintegration.utils import setup_cmempy_user_access


class DatasetParameterType(StringParameterType):
    """Dataset parameter type."""

    allow_only_autocompleted_values: bool = True

    autocomplete_value_with_labels: bool = True

    dataset_type: Optional[str] = None

    def __init__(self, dataset_type: str = None):
        """Dataset parameter type."""
        self.dataset_type = dataset_type

    def label(self, value: str, context: PluginContext) -> Optional[str]:
        """Returns the label for the given dataset."""
        setup_cmempy_user_access(context.user)
        task_label = str(
            get_task(project=context.project_id, task=value)["metadata"]["label"]
        )
        return f"{task_label}"

    def autocomplete(self, query_terms: list[str],
                     depend_on_parameter_values: list[str],
                     context: PluginContext) -> list[Autocompletion]:
        setup_cmempy_user_access(context.user)
        datasets = list_items(item_type="dataset",
                              project=context.project_id)["results"]

        result = []
        for _ in datasets:
            identifier = _['id']
            title = _["label"]
            label = f"{title} ({identifier})"
            if self.dataset_type is not None and self.dataset_type != _["pluginId"]:
                # Ignore datasets of other types
                continue
            for term in query_terms:
                if term.lower() in label.lower():
                    result.append(Autocompletion(value=identifier, label=label))
            if len(query_terms) == 0:
                # add any dataset to list if no search terms are given
                result.append(Autocompletion(value=identifier, label=label))
        result.sort(key=lambda x: x.label)  # type: ignore
        return list(set(result))
