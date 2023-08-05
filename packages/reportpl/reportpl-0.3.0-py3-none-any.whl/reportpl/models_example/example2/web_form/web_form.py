from reportpl.widgets import TextWidget
from reportpl.types import ValidationError
from reportpl.web_converters import DateConverter
from reportpl.base_web_form import BaseWebForm



class Form(BaseWebForm):
    
    def define_widgets(self):
        self.widgets = [
            [
                TextWidget(self, 'nome', default="", placeholder="Digite seu nome",required=True),
                TextWidget(self, 'data_nascimento', label="Data de nascimento",converters=[DateConverter()]),
            ],
        ]