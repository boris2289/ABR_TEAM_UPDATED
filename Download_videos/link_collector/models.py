from django.db import models


class Resolution:
    def __init__(self):
        self.resolution = []
        self.mistakes = Mistakes()

    def add_resolution(self, text: str):
        self.resolution.append(text)

    def clear_resolutions(self):
        self.resolution.clear()

    def has_resolutions(self) -> bool:
        return len(self.resolution) > 0

    def __str__(self):
        return f'Resolutions: {self.resolution}\nMistakes: {self.mistakes}'


class Mistakes:
    def __init__(self):
        self.mistakes = {}

    def add_mistake(self, key: str, description: str):
        self.mistakes[key] = description

    def remove_mistake(self, key: str):
        if key in self.mistakes:
            del self.mistakes[key]

    def has_mistakes(self) -> bool:
        return len(self.mistakes) > 0

    def clear_mistakes(self):
        self.mistakes.clear()

    def __str__(self):
        return f'{self.mistakes}'


class Link:
    def __init__(self):
        self.link = ''

    def set_link(self, url: str):
        self.link = url

    def clear_link(self):
        self.link = ''

    def is_empty(self) -> bool:
        return self.link == ''

    def __str__(self):
        return f'Link: {self.link}'
