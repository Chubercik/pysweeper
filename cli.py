from typing import Tuple


class Text:
    """
    Class representing text.
    """
    def __init__(self,
                 text: str = '',
                 bold: bool = False,
                 italic: bool = False,
                 foreground_color: Tuple[str] = None,
                 background_color: Tuple[str] = None):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.foreground_color = foreground_color
        self.background_color = background_color

    def bold_string(self,
                    text: str,
                    bold: bool) -> str:
        """
        Adds bold styling to the given text.
        """
        return f"\033[1m{text}\033[0m" if bold else text

    def foreground_color_string(self,
                                text: str,
                                foreground_color: Tuple[str]) -> str:
        """
        Adds foreground color to the given text.
        """
        r, g, b = foreground_color
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def background_color_string(self,
                                text: str,
                                background_color: Tuple[str]) -> str:
        """
        Adds background color to the given text.
        """
        r, g, b = background_color
        return f"\033[48;2;{r};{g};{b}m{text}\033[0m"

    def italic_string(self,
                      text: str,
                      italic: bool) -> str:
        """
        Adds italic styling to the given text.
        """
        return f"\033[3m{text}\033[0m" if italic else text

    def __str__(self) -> str:
        """
        Returns a string representation of the text.
        """
        text = self.text
        if self.bold:
            text = self.bold_string(text, self.bold)
        if self.foreground_color:
            text = self.foreground_color_string(text, self.foreground_color)
        if self.background_color:
            text = self.background_color_string(text, self.background_color)
        if self.italic:
            text = self.italic_string(text, self.italic)
        return text


test = Text(text='test', bold=True, italic=True, foreground_color=(255, 0, 0), background_color=(0, 255, 0))
print(test)
