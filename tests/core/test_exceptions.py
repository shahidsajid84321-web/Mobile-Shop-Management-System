import pytest

from app.core.exceptions import (
    AppException,
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
)


def test_custom_exceptions_are_app_exceptions():
    assert isinstance(BadRequestException("bad"), AppException)
    assert isinstance(NotFoundException("missing"), AppException)
    assert isinstance(UnauthorizedException("unauthorized"), AppException)
    assert isinstance(ForbiddenException("forbidden"), AppException)


def test_custom_exceptions_preserve_messages():
    assert str(BadRequestException("bad")) == "bad"
    assert str(NotFoundException("missing")) == "missing"
    assert str(UnauthorizedException("unauthorized")) == "unauthorized"
    assert str(ForbiddenException("forbidden")) == "forbidden"


def test_custom_exceptions_can_be_raised():
    with pytest.raises(BadRequestException, match="bad"):
        raise BadRequestException("bad")

    with pytest.raises(NotFoundException, match="missing"):
        raise NotFoundException("missing")

    with pytest.raises(UnauthorizedException, match="unauthorized"):
        raise UnauthorizedException("unauthorized")

    with pytest.raises(ForbiddenException, match="forbidden"):
        raise ForbiddenException("forbidden")