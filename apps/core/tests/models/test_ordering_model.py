import pytest

from core.tests.decorators import temporary_models
from core.tests.factories import ChildFactory, ParentFactory


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model])
def test_ordering_model_parent_create():
    ParentFactory.create_batch(3)
    ordering = (
        ParentFactory._meta.model
        .objects
        .values_list('ordering_number', flat=True)
        .order_by('ordering_number')
    )

    assert list(ordering) == list(range(1, 4))


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model])
def test_ordering_model_parent_move_up():
    parents = ParentFactory.create_batch(3)
    ordering = (
        ParentFactory._meta.model
        .objects
        .values_list('pk', flat=True)
        .order_by('ordering_number')
    )

    ParentFactory._meta.model.objects.move(parents[0], 3)
    assert list(ordering) == [parents[i].pk for i in range(1, 3)] + [parents[0].pk]


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model])
def test_ordering_model_parent_move_down():
    parents = ParentFactory.create_batch(3)
    ordering = (
        ParentFactory._meta.model
        .objects
        .values_list('pk', flat=True)
        .order_by('ordering_number')
    )

    ParentFactory._meta.model.objects.move(parents[2], 1)
    assert list(ordering) == [parents[2].pk] + [parents[i].pk for i in range(0, 2)]


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model, ChildFactory._meta.model])
def test_ordering_model_child_move():
    parent1 = ParentFactory.create()
    parent2 = ParentFactory.create()

    children1 = ChildFactory.create_batch(3, parent=parent1)
    children2 = ChildFactory.create_batch(3, parent=parent2)

    ordering = (
        ChildFactory._meta.model
        .objects
        .values_list('pk', flat=True)
        .order_by('ordering_number')
    )

    ChildFactory._meta.model.objects.move(children1[0], 3)
    ChildFactory._meta.model.objects.move(children2[2], 1)

    assert list(ordering.filter(parent=parent1)) == [children1[1].pk, children1[2].pk, children1[0].pk]
    assert list(ordering.filter(parent=parent2)) == [children2[2].pk, children2[0].pk, children2[1].pk]


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model, ChildFactory._meta.model])
def test_ordering_model_child_create():
    parent1 = ParentFactory()
    ChildFactory.create_batch(3, parent=parent1)

    ordering = (
        ChildFactory._meta.model
        .objects
        .values_list('ordering_number', flat=True)
        .order_by('ordering_number')
    )

    assert list(ordering) == list(range(1, 4))

    parent2 = ParentFactory()
    ChildFactory.create_batch(3, parent=parent2)
    ordering = ordering.filter(parent=parent2)

    assert list(ordering) == list(range(1, 4))


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model])
def test_ordering_model_parent_delete():
    parent1 = ParentFactory()
    parent2 = ParentFactory()

    parent1.delete()
    parent2.refresh_from_db()
    assert parent2.ordering_number == 1

    parent3 = ParentFactory()
    parent3.delete()
    parent2.refresh_from_db()
    assert parent2.ordering_number == 1


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model])
def test_ordering_model_child_delete():
    parent1 = ParentFactory()
    children1 = ChildFactory.create_batch(3, parent=parent1)

    parent2 = ParentFactory()
    children2 = ChildFactory.create_batch(3, parent=parent2)

    children1[1].delete()
    children2[1].delete()

    ordering = (
        ChildFactory._meta.model
        .objects
        .values_list('ordering_number', flat=True)
        .order_by('ordering_number')
    )

    assert list(ordering.filter(parent=parent1)) == [1, 2]
    assert list(ordering.filter(parent=parent2)) == [1, 2]


@pytest.mark.django_db
@temporary_models([ParentFactory._meta.model])
def test_ordering_model_parent_move_invalid():
    parent1 = ParentFactory()
    parent2 = ParentFactory()

    ParentFactory._meta.model.objects.move(parent1, 3)
    parent1.refresh_from_db()
    parent2.refresh_from_db()

    assert parent1.ordering_number == 1
    assert parent2.ordering_number == 2

    ParentFactory._meta.model.objects.move(parent2, 0)

    assert parent1.ordering_number == 1
    assert parent2.ordering_number == 2
