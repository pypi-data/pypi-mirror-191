import abc
import contextvars
import typing
import time
import uuid

VERSION = "0.1.0"

T = typing.TypeVar("T")


class TraceIdNotYetSetError(Exception):
    """
    Raised when trying to get a traceid that hasn't been set.
    Please use TraceId.gen() to generate a new traceid or TraceId.set() to set an existing traceid.
    """

    pass


class TraceId(typing.Generic[T]):
    traceid_var = contextvars.ContextVar[T]("__traceid__")

    @classmethod
    def set(cls, traceid: T) -> None:
        """
        Set the traceid for the current context.
        Args:
            traceid: The traceid to set. Cannot be None.
        Returns:
            None
        """
        if traceid is None:
            raise ValueError("TraceId cannot be set to None.")
        cls.traceid_var.set(traceid)

    @classmethod
    def get(cls) -> T:
        """
        Get the traceid for the current context.
        Returns:
            The traceid for the current context.
        """
        try:
            id = cls.traceid_var.get()
            if id is None:
                raise TraceIdNotYetSetError(
                    "TraceId is not yet set. Please use TraceId.gen() to generate a new traceid or TraceId.set() to set an existing traceid."
                )
            return id
        except LookupError:
            raise TraceIdNotYetSetError(
                "TraceId is not yet set. Please use TraceId.gen() to generate a new traceid or TraceId.set() to set an existing traceid."
            )

    @classmethod
    def clear(cls) -> None:
        """
        Clear the traceid for the current context.
        Returns:
            None
        """
        cls.traceid_var.set(None)  # type: ignore

    @classmethod
    def is_set(cls) -> bool:
        """
        Check if the traceid is set for the current context.
        Returns:
            True if the traceid is set, False otherwise.
        """
        return cls.traceid_var.get(None) is not None

    @abc.abstractclassmethod
    def gen(cls) -> T:
        """
        Generate and set a new traceid.
        """
        raise NotImplementedError


class UUIDTraceId(TraceId[uuid.UUID]):
    """
    A traceid that is a UUID.
    """

    @classmethod
    def gen(cls):
        """
        Generate and set a new UUID traceid.
        """
        if not cls.is_set():
            cls.set(uuid.uuid4())


class NanosecondTraceId(TraceId[int]):
    @classmethod
    def gen(cls):
        """
        Set current time in nanoseconds as traceid.
        """
        if not cls.is_set():
            cls.set(time.time_ns())


class RandomStrTraceId(TraceId[str]):
    @classmethod
    def gen(cls):
        """
        Generate and set a new random string traceid.
        """
        if not cls.is_set():
            cls.set(str(uuid.uuid4()))
