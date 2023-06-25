from typing import Any
from infra.cross_cutting.parsers.parser import from_dict


class GenericJsonToViewModelMapping:
    """Provides a named configuration for all view model object maps."""

    @staticmethod
    def to_view_model(json: dict, view_model_class: Any) -> Any:
        """Parses a input JSON object to a view model class.

        Args:
            json (dict): The JSON object.
            view_model_class (Any): The target class. It must be a view model.

        Returns:
            Any: A view model object.
        """
        return from_dict(view_model_class, json)
