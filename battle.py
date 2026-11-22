from ex3 import (
    CreatureFactory,
    FlameFactory,
    TransformCreatureFactory,
)


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")

    base_creature = factory.create_base()
    print(base_creature.describe())
    print(base_creature.attack())

    evolved_creature = factory.create_evolved()
    print(evolved_creature.describe())
    print(evolved_creature.attack())


def test_battle(
    factory1: CreatureFactory,
    factory2: CreatureFactory,
) -> None:
    print("Testing battle")
    base_creature1 = factory1.create_base()
    base_creature2 = factory2.create_base()

    print(base_creature1.describe())
    print(" vs.")
    print(base_creature2.describe())
    print(" fight!")
    print(base_creature1.attack())
    print(base_creature2.attack())


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    test_factory(flame_factory)
    print()
    test_factory(transform_factory)
    print()
    test_battle(flame_factory, transform_factory)
    print()


if __name__ == "__main__":
    main()
