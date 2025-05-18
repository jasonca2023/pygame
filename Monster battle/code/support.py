from settings import *
import os

def folder_importer(*path):
    surfs = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
                full_path = join(folder_path, file_name)
                surfs[file_name.split('.')[0]] = pygame.image.load(full_path).convert_alpha()
    return surfs

def audio_importer(*path):
    audio_dict = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
            if '.mp3' in file_name or '.wav' in file_name:
                audio_dict[file_name.split('.')[0]] = pygame.mixer.Sound(join(folder_path, file_name))
    audio_dict['music'].set_volume(0.8)
    audio_dict['fire'].set_volume(0.4)
    audio_dict['ice'].set_volume(0.2)
    audio_dict['explosion'].set_volume(1.2)
    audio_dict['heal'].set_volume(0.3)
    audio_dict['green'].set_volume(0.1)
    audio_dict['splash'].set_volume(0.2)
    audio_dict['scratch'].set_volume(0.3)
    return audio_dict

def tile_importer(cols, *path):
    attack_frames = {}
    for folder_path, _, file_names in walk(join(*path)):
        for file_name in file_names:
                full_path = join(folder_path, file_name)
                surf = pygame.image.load(full_path).convert_alpha()
                attack_frames[file_name.split('.')[0]] = []
                cutout_width = surf.get_width() / cols
                for col in range(cols):
                    cutout_surf = pygame.Surface((cutout_width, surf.get_height()), pygame.SRCALPHA)
                    cutout_rect = pygame.FRect(cutout_width * col, 0, cutout_width, surf.get_height())
                    cutout_surf.blit(surf, (0, 0), cutout_rect)
                    attack_frames[file_name.split('.')[0]].append(cutout_surf)
    return attack_frames
