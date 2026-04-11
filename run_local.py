"""Run the Ethical Twin environment locally using a simple smart policy."""

from __future__ import annotations

from policy import smart_policy
from server.environment import EnvironmentService


def _dump(model) -> dict:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def main() -> None:
    service = EnvironmentService()
    state = service.reset()

    print("Initial state:")
    print(_dump(state))
    print()

    current_observation = _dump(state)["observation"]

    while not state.done:
        action = smart_policy(current_observation)
        result = service.step(action)
        result_data = _dump(result)
        state = result.state
        current_observation = result_data["observation"]

        print(f"Observation: {current_observation}")
        print(f"Chosen action: {action}")
        print(f"Reward: {result_data['reward']}")
        print()

    print("Episode finished after 10 steps.")


if __name__ == "__main__":
    main()
