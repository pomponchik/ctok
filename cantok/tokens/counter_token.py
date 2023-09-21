from threading import RLock

from cantok.tokens.abstract_token import AbstractToken
from cantok import ConditionToken


class CounterToken(ConditionToken):
    def __init__(self, counter: int, *tokens: AbstractToken, cancelled: bool = False):
        if counter < 0:
            raise ValueError('The counter must be greater than or equal to zero.')

        self.counter = counter
        self.lock = RLock()

        def function() -> bool:
            with self.lock:
                if not self.counter:
                    return True
                self.counter -= 1
                return False

        super().__init__(function, *tokens, cancelled=cancelled)

    def __repr__(self):
        other_tokens = ', '.join([repr(x) for x in self.tokens])
        if other_tokens:
            other_tokens += ', '
        superpower = self.text_representation_of_superpower() + ', '
        cancelled = self.get_cancelled_status_without_decrementing_counter()
        return f'{type(self).__name__}({superpower}{other_tokens}cancelled={cancelled})'

    def __str__(self):
        cancelled_flag = 'cancelled' if self.get_cancelled_status_without_decrementing_counter() else 'not cancelled'
        return f'<{type(self).__name__} ({cancelled_flag})>'

    def get_cancelled_status_without_decrementing_counter(self) -> bool:
        with self.lock:
            result = self.cancelled
            if not result:
                self.counter += 1
            return result

    def is_cancelled_reflect(self):
        return self.get_cancelled_status_without_decrementing_counter()

    def text_representation_of_superpower(self) -> str:
        return str(self.counter)

    def text_representation_of_extra_kwargs(self) -> str:
        return ''