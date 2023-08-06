from kabaret import flow
from libreflow.baseflow.film import Film as BaseFilm


class CreateKitsuSequences(flow.Action):

    ICON = ('icons.libreflow', 'kitsu')

    skip_existing = flow.SessionParam(False).ui(editor='bool')
    create_shots = flow.SessionParam(False).ui(editor='bool')

    _film = flow.Parent()

    def get_buttons(self):
        return ['Create sequences', 'Cancel']
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        sequences_data = self.root().project().kitsu_api().get_sequences_data()
        create_shots = self.create_shots.get()
        skip_existing = self.skip_existing.get()

        for data in sequences_data:
            name = data['name'].lower()

            if not self._film.sequences.has_mapped_name(name):
                s = self._film.sequences.add(name)
            elif not skip_existing:
                s = self._film.sequences[name]
            else:
                continue
            
            print(f'Create sequence {data["name"]}')

            if create_shots:
                s.create_shots.skip_existing.set(skip_existing)
                s.create_shots.run('Create shots')
        
        self._film.sequences.touch()


class Film(BaseFilm):

    create_sequences = flow.Child(CreateKitsuSequences)
