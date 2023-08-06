"""Contains the implementation of the job client."""

import os
from types import TracebackType
from typing import Any

import grpc
from spm_pb2 import RefreshRequest, Token
from spm_pb2_grpc import TokenManagerStub

from . import defaults
from .auth import AccessTokenAuthMetadataPlugin


class JobClient:
    """The JobClient is the recommended way to connect to the numerous platform."""

    def __init__(self, channel: grpc.Channel):
        self._channel = channel

    @staticmethod
    def channel_options() -> list[tuple[str, Any]]:
        """Return the default gRPC channel options."""
        return [
            ("grpc.max_message_length", defaults.GRPC_MAX_MESSAGE_SIZE),
            ("grpc.max_send_message_length", defaults.GRPC_MAX_MESSAGE_SIZE),
            ("grpc.max_receive_message_length", defaults.GRPC_MAX_MESSAGE_SIZE),
        ]

    @staticmethod
    def create(hostname: str, port: str, refresh_token: str) -> "JobClient":
        """Create a JobClient from connection parameters.

        :param hostname: Hostname of the numerous server
        :param port: gRPC port of the numerous server
        :param refresh_token: Refresh token for the execution.
        """
        with grpc.secure_channel(
            f"{hostname}:{port}",
            grpc.ssl_channel_credentials(),
            JobClient.channel_options(),
        ) as unauthorized_channel:
            token_manager = TokenManagerStub(unauthorized_channel)
            access_token = token_manager.GetAccessToken(
                RefreshRequest(refresh_token=Token(val=refresh_token))
            )

        authorized_channel = grpc.secure_channel(
            f"{hostname}:{port}",
            grpc.composite_channel_credentials(
                grpc.ssl_channel_credentials(),
                grpc.metadata_call_credentials(
                    AccessTokenAuthMetadataPlugin(access_token.val)
                ),
            ),
            JobClient.channel_options(),
        )

        return JobClient(authorized_channel)

    @staticmethod
    def from_environment() -> "JobClient":
        """Create a JobClient from environment variables.

        Uses the following environment variables:
         - `NUMEROUS_API_SERVER`
         - `NUMEROUS_API_PORT`
         - `NUMEROUS_API_REFRESH_TOKEN`
        """
        return JobClient.create(
            os.environ["NUMEROUS_API_SERVER"],
            os.environ["NUMEROUS_API_PORT"],
            os.environ["NUMEROUS_API_REFRESH_TOKEN"],
        )

    def close(self) -> None:
        """Close the JobClient.

        Closes the JobClient's connection to the numerous platform, immediately
        terminating any active communication.

        This method is idempotent.
        """
        self._channel.close()

    def __enter__(self) -> "JobClient":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,  # noqa: F841
        exc_value: BaseException | None,  # noqa: F841
        traceback: TracebackType | None,  # noqa: F841
    ) -> bool | None:
        self.close()
        return None
