from kabaret import flow
from libreflow.baseflow.shot import ShotCollection, Shot as BaseShot, Sequence as BaseSequence
from libreflow.baseflow.task import ManagedTaskCollection


class Shot(BaseShot):
    
    tasks = flow.Child(ManagedTaskCollection).ui(
        expanded=True,
        show_filter=True
    )
    
    def ensure_tasks(self):
        """
        Creates the tasks of this shot based on the task
        templates of the project, skipping any existing task.
        """
        mgr = self.root().project().get_task_manager()

        for dt in mgr.default_tasks.mapped_items():
            if (
                not self.tasks.has_mapped_name(dt.name())
                and not dt.optional.get()
                and dt.template.get() == 'shot'
            ):
                t = self.tasks.add(dt.name())
                t.enabled.set(dt.enabled.get())
        
        self.tasks.touch()


class Shots(ShotCollection):

    def add(self, name, object_type=None):
        """
        Adds a shot to the global shot collection, and creates
        its tasks.
        """
        s = super(Shots, self).add(name, object_type)
        s.ensure_tasks()

        return s


class CreateKitsuShots(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')

    _sequence = flow.Parent()

    def get_buttons(self):
        return ['Create shots', 'Cancel']

    def allow_context(self, context):
        return context and context.endswith('.details')
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        skip_existing = self.skip_existing.get()
        shots_data = self.root().project().kitsu_api().get_shots_data(self._sequence.name())
        for data in shots_data:
            name = data['name'].lower()

            if not self._sequence.shots.has_mapped_name(name):
                s = self._sequence.shots.add(name)
            elif not skip_existing:
                s = self._sequence.shots[name]
            else:
                continue
            
            print(f'Create shot {self._sequence.name()} {data["name"]}')
        
        self._sequence.shots.touch()


class Sequence(BaseSequence):
    
    shots = flow.Child(Shots).ui(expanded=True)

    create_shots = flow.Child(CreateKitsuShots)
