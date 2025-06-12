from django import forms
from .models import Customer,Activity
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django.forms.widgets import TextInput


TAIWAN_CITIES = [
    ('台北市', '台北市'), ('新北市', '新北市'), ('桃園市', '桃園市'), ('台中市', '台中市'),
    ('台南市', '台南市'), ('高雄市', '高雄市'), ('基隆市', '基隆市'), ('新竹市', '新竹市'),
    ('新竹縣', '新竹縣'), ('苗栗縣', '苗栗縣'), ('彰化縣', '彰化縣'), ('南投縣', '南投縣'),
    ('雲林縣', '雲林縣'), ('嘉義市', '嘉義市'), ('嘉義縣', '嘉義縣'), ('屏東縣', '屏東縣'),
    ('宜蘭縣', '宜蘭縣'), ('花蓮縣', '花蓮縣'), ('台東縣', '台東縣'), ('澎湖縣', '澎湖縣'),
    ('金門縣', '金門縣'), ('連江縣', '連江縣'),
]


class CustomerForm(forms.ModelForm):
    city = forms.ChoiceField(choices=TAIWAN_CITIES, required=False, label="縣市")
    class Meta:
        model = Customer
       # fields = ['name', 'email', 'phone', 'gender', 'city', 'district', 'photo', 'constellation', 'birthday_md', 'note']
        fields = '__all__'

        labels = {
            'name': '姓名',
            'email': 'Email',
            'phone': '電話',
            'gender': '性別',
            'city': '縣市',
            'district': '鄉鎮區',
            'note': '備註',
            'constellation' :'星座',
            'birthday_md' : '生日'
        }
        widgets = {
            'gender': forms.RadioSelect,
            'birthday_md': TextInput(attrs={'placeholder': 'MM-DD'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('phone', css_class='col-md-6'),
                Column('gender', css_class='col-md-6'),
            ),
            Row(
                Column('city', css_class='col-md-6'),
                Column('district', css_class='col-md-6'),
            ),
            Row(
                Column('note', css_class='col-12'),
            ),
            Row(
                Column('photo', css_class='col-12'),
            ),
            Row(
                Column('constellation', css_class='col-md-6'),
            ),
            Row(
            Column('birthday_md', css_class='col-md-6'),
        ),
        )
        if not self.instance.pk:
            self.fields['note'].initial = "家庭：\n職業：\n興趣："
        

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['type', 'date', 'content']

