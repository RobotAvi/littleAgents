import importlib
import asyncio
import pytest

# Список утилит и их путей
UTILITIES = [
    'utilities.infrastructure_monitor.app',
    'utilities.materials_prep.app',
    'utilities.meeting_conductor.app',
    'utilities.meeting_prep.app',
    'utilities.messenger_analyzer.app',
    'utilities.personal_tasks.app',
    'utilities.process_optimizer.app',
    'utilities.project_manager.app',
    'utilities.reputation_manager.app',
    'utilities.travel_organizer.app',
    'utilities.calendar_manager.app',
    'utilities.crm_manager.app',
    'utilities.email_manager.app',
    'utilities.event_organizer.app',
    'utilities.finance_admin.app',
    'utilities.git_monitor.app',
    'utilities.hr_communications.app',
]

@pytest.mark.parametrize("module_path", UTILITIES)
def test_utility_main(module_path):
    mod = importlib.import_module(module_path)
    main_func = getattr(mod, "main", None)
    assert main_func is not None, f"{module_path} has no main()"
    if asyncio.iscoroutinefunction(main_func):
        asyncio.run(main_func())
    else:
        main_func()