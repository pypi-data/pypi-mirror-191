import re

from lupin_grognard.core.commit.commit import Commit
from lupin_grognard.core.commit.commit_reporter import CommitReporter
from lupin_grognard.core.commit.commit_error import ErrorCount
from lupin_grognard.core.config import (
    COMMIT_TYPE_MUST_HAVE_SCOPE,
    COMMIT_TYPE_MUST_NOT_HAVE_SCOPE,
    INITIAL_COMMIT,
    PATTERN,
    TITLE_FAILED,
)


class CommitValidator(Commit):
    def __init__(self, commit: str, error_counter: ErrorCount):
        super().__init__(commit=commit)
        self.reporter = CommitReporter(commit=commit)
        self.error_counter = error_counter

    def perform_checks(self, merge_option: bool) -> None:
        if merge_option:  # check merge commits have approvers
            if self._is_merge_commit(self.title):
                if not self._validate_commit_merge():
                    self.error_counter.increment_merge_error()
            else:
                if not self._validate_commit_title():
                    self.error_counter.increment_title_error()
                if not self._validate_body():
                    self.error_counter.increment_body_error()
        else:
            if not self._validate_commit_title():
                self.error_counter.increment_title_error()
            if not self._is_merge_commit(self.title):
                if not self._validate_body():
                    self.error_counter.increment_body_error()

    def _validate_commit_title(self) -> bool:
        if self._validate_commit_message(self.title):
            self.reporter.display_valid_title_report()
            return True
        else:
            return False

    def _validate_body(self) -> bool:
        if self.body:
            message_error = []
            for message in self.body:
                if self._validate_body_message(message=message):
                    message_error.append(message)
            if len(message_error) > 0:
                self.reporter.display_body_report(messages=message_error)
                return False  # must not start with a conventional message
        return True

    def _validate_commit_message(self, commit_msg: str):
        if self._is_special_commit(commit_msg=commit_msg):
            return True

        type, scope = self._get_conventional_commit_type_and_scope(
            commit_msg=commit_msg
        )
        match type:
            case None:
                self.reporter.display_invalid_title_report(error_message=TITLE_FAILED)
                return False
            case "feat":
                return self._validate_commit_message_for_feat_type(scope=scope)
            case _:
                return self._validate_commit_message_for_generic_type(
                    type=type, scope=scope
                )

    def _validate_body_message(self, message: str) -> bool:
        """Validates a body message does not start with a conventional commit message"""
        return bool(re.match(PATTERN, message))

    def _is_special_commit(self, commit_msg: str) -> bool:
        return (
            commit_msg.startswith(("Merge", "Revert", "fixup!", "squash!"))
            or commit_msg in INITIAL_COMMIT
        )

    def _is_merge_commit(self, commit_msg: str) -> bool:
        return commit_msg.startswith("Merge")

    def _validate_commit_merge(self) -> bool:
        self.reporter.display_merge_report(approvers=self.approvers)
        if len(self.approvers) < 1:
            return False
        return True

    def _get_conventional_commit_type_and_scope(self, commit_msg: str) -> tuple:
        """Returns the conventional commit type and scope if present"""
        match = re.match(PATTERN, commit_msg)
        if match:
            type, scope = match.groups()[:2]
            return type, scope
        return None, None

    def _validate_commit_message_for_feat_type(self, scope: str) -> bool:
        """Validates the scope for a feat commit"""
        if scope is None or scope not in ["(add)", "(change)", "(remove)"]:
            self.reporter.display_invalid_title_report(
                error_message=COMMIT_TYPE_MUST_HAVE_SCOPE
            )
            return False
        else:
            return True

    def _validate_commit_message_for_generic_type(self, type, scope: str) -> bool:
        """Validates other commit types do not contain a scope"""
        if scope is None:
            return True
        else:
            error_message = COMMIT_TYPE_MUST_NOT_HAVE_SCOPE.format(type, type)
            self.reporter.display_invalid_title_report(error_message=error_message)
            return False
