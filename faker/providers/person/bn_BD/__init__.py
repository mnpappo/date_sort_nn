# coding=utf-8
from __future__ import unicode_literals
from .. import Provider as PersonProvider


class Provider(PersonProvider):
    formats = (
        '{{first_name_male}} {{last_name_male}}',
        '{{first_name_male}} {{last_name_male}}',
        '{{first_name_male}} {{last_name_male}}',
        '{{first_name_male}} {{last_name_male}}',
        '{{first_name_male}} {{last_name_male}}',
        '{{first_name_female}} {{last_name_female}}',
        '{{first_name_female}} {{last_name_female}}',
        '{{first_name_female}} {{last_name_female}}',
        '{{first_name_female}} {{last_name_female}}',
        '{{first_name_female}} {{last_name_female}}',
        '{{prefix_male}} {{first_name_male}} {{last_name_male}}',
        '{{prefix_female}} {{first_name_female}} {{last_name_female}}',
        '{{first_name_male}} {{last_name_male}} {{suffix}}',
        '{{first_name_female}} {{last_name_female}} {{suffix}}',
        '{{prefix_male}} {{first_name_male}} {{last_name_male}} {{suffix}}',
        '{{prefix_female}} {{first_name_female}} {{last_name_female}} {{suffix}}'
    )


    first_names_male = (
         'মহিউদ্দিন' , 'হামিদুর' , 'মস্তাফা' , 'রহুল' , 'মতিউর' , 'হামিদুর' ,'নূর' , 'আব্বদুর', 'রফিক', 'সালাম' , 'বরকত' ,'জব্বার', 'আবুল' ,
         'মনিরুজজামান' , 'জাকারিয়া' , 'কাওসার' , 'সুমন' ,'আশিক' ,'রাসেল' ,'রাফি' ,'আপন', 'সাগর' , 'সৈকত' , 'শামিম' ,'আরিফ', 'মামুন',
         'শরিফ' ,'মবিন' , 'বুলবুল' , 'জয়' , 'রুবেল' , 'নাবিল' , 'সিফাত' , 'নাফিস' , 'অনন্ত' , 'জলিল' ,'মান্না' , 'কাবিলা'
    )

    first_names_female = (
        'বেগম', 'আশা' , 'দিশা' , 'সুফিয়া' , 'সাঞ্জিদা' , 'বুশ্রা' , 'পপি' , 'আবিদা' , 'রুনা' , 'সাবিনা' , 'টুম্পা' , 'টিনা' ,'মিনা' ,'আনিকা' ,
         'সাদিয়া' , 'মুন' , 'পূজা' , 'ফারিয়া' , 'কাকলী' , 'রাবু' , 'তমা' , 'জবা' ,'জেসমিন' , 'কণা' , 'অর্পিতা' , 'মৌ' , 'লিজা' , 'বীণা' ,
         'শারিকা' , 'হৃদি' ,  'জুই', 'সাবিলা', 'কেয়া' , 'শাবানা', 'বর্ষা', 'লাবনী', 'সুমা'
    )

    first_names = first_names_male + first_names_female

    last_names_male = (
        'বাতেন', 'জাহাঙ্গীর', 'রহমান', 'কামাল', 'আমিন' ,'খন্দকার', 'উল্লা', 'বাতেন', 'মনির' , 'আহমেদ', 'ইসলাম', 'রহমান', 'হাস্নাত'
    )

    last_names_female = (
        'রকিয়া' ,'কামাল', 'খানন', 'আখতার', 'লাইলা', 'ইয়াসমিন', 'আফরোজা', 'জামান', 'তাস্নিম', 'হারুন', 'তাবাসসুম'
    )

    last_names = last_names_male + last_names_female


    prefixes_male = ('মোহাম্মাদ', 'মিঃ')

    prefixes_female = ('মিস', 'মিসেস' )

    suffixes = ('শেখ', 'মিয়া' , 'খান', 'বিশসাস', 'হোসেন', 'ইসলাম')
