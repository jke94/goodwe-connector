from goodwe_connector.goodwe_context import GoodweContext


class FakeStrategy:
    def __init__(self):
        self.calls = []

    def do_algorithm(self, goodwe):
        self.calls.append(goodwe)
        return {"ok": True}


def test_goodwe_context_process_uses_the_assigned_strategy():
    # Arrange
    fake_goodwe_api = object()
    strategy = FakeStrategy()
    context = GoodweContext(goodwe_api=fake_goodwe_api, strategy=strategy)

    # Act
    result = context.process()

    # Assert
    assert result == {"ok": True}
    assert strategy.calls == [fake_goodwe_api]
