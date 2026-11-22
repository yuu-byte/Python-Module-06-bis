from ex3 import TransformCreatureFactory


def main() -> None:
    print("Testing Creature with transform capability")
    transform_factory = TransformCreatureFactory()
    base_creature = transform_factory.create_base()
    evolved_creature = transform_factory.create_evolved()
    print(" base:")
    print(base_creature.describe())
    print(base_creature.attack())
    print(base_creature.transform())
    print(base_creature.attack())
    print(base_creature.revert())

    print(" evolved:")
    print(evolved_creature.describe())
    print(evolved_creature.attack())
    print(evolved_creature.transform())
    print(evolved_creature.attack())
    print(evolved_creature.revert())


if __name__ == "__main__":
    main()
