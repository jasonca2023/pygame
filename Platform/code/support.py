from settings import *

def import_image(*path, format = 'png', alpha = True):
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path):
    frames = []
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
            full_path = join(folder_path, file_name)
            frames.append(pygame.image.load(full_path).convert_alpha())
    return frames

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            if '.wav' in file_name or '.ogg' in file_name:
                full_path = join(folder_path, file_name)
                audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(full_path)
    audio_dict['music'].set_volume(0.7)
    audio_dict['impact'].set_volume(0.1)
    audio_dict['shoot'].set_volume(0.1)
    return audio_dict
