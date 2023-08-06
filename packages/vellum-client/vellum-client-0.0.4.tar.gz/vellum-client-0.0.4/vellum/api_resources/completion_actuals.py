from dataclasses import asdict
from typing import List, Optional

from vellum.api_resources.abstract.predict_api_resource import PredictAPIResource
from vellum.api_resources.types import CompletionActual, SubmitCompletionActualsResult


class SubmitCompletionActuals(PredictAPIResource):
    api_path = "v1/submit-completion-actuals"

    @classmethod
    def run(  # type: ignore
        cls,
        actuals: List[CompletionActual],
        deployment_id: Optional[str] = None,
        deployment_name: Optional[str] = None,
    ) -> SubmitCompletionActualsResult:
        """Submit actuals for previously made completion requests.

        Args:
            actuals: A list of CompletionActual objects, each containing the info needed
                to submit a single actual.
            deployment_id: The ID of the deployment that the completion came from. You must provide either this
                or deployment_name.
            deployment_name: The name of the deployment that the completion came from. You must provide either
                this or deployment_id.
        Returns:
            The result of the generation request.
        """

        if deployment_id is None and deployment_name is None:
            raise ValueError("Must provide either deployment_id or deployment_name")
        elif deployment_id is not None and deployment_name is not None:
            raise ValueError("Must provide only one of deployment_id or deployment_name")

        super().run(
            actuals=[asdict(actual) for actual in actuals],
            deployment_id=deployment_id,
            deployment_name=deployment_name,
        )

        return SubmitCompletionActualsResult(success=True)
