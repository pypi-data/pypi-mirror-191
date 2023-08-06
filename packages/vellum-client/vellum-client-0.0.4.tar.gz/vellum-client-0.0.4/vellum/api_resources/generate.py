from dataclasses import asdict
from typing import Any, Dict, List, Optional

from vellum.api_resources.abstract.predict_api_resource import PredictAPIResource
from vellum.api_resources.types import GenerateRequest, GenerateResult


class Generate(PredictAPIResource):
    api_path = "v1/generate"

    @classmethod
    def run(  # type: ignore
        cls,
        requests: List[GenerateRequest],
        deployment_id: Optional[str] = None,
        deployment_name: Optional[str] = None,
    ) -> GenerateResult:
        """Run a generation request against Vellum's predict API.

        Args:
            requests: A list of GenerationRequest objects, each containing the info needed
                to make a single prediction.
            deployment_id: The ID of the deployment to use for generating predictions. You must provide either this
                or deployment_name.
            deployment_name: The name of the deployment to use for generating predictions. You must provide either
                this or deployment_id.
        Returns:
            The result of the generation request.
        """

        if deployment_id is None and deployment_name is None:
            raise ValueError("Must provide either deployment_id or deployment_name")
        elif deployment_id is not None and deployment_name is not None:
            raise ValueError("Must provide only one of deployment_id or deployment_name")

        raw_result = super().run(
            requests=[asdict(request) for request in requests],
            deployment_id=deployment_id,
            deployment_name=deployment_name,
        )

        return GenerateResult.from_raw(raw_result)
