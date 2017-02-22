# coding=utf-8
from __future__ import unicode_literals
from .. import Provider as AddressProvider


class Provider(AddressProvider):

    city_formats = ('{{city_name}}', )

    street_name_formats = ('{{street_name}}', )
    street_address_formats = ('{{street_name}} {{building_number}}', )
    address_formats = ('{{street_address}}\n{{postcode}} {{city}}', )

    building_number_formats = ('###', '##', '#', '#/#')

    street_suffixes_long = ('রোড', )
    street_suffixes_short = ('রোঃ', )

    postcode_formats = ('### ##', )

    cities = (
        'ঢাকা', 'ইসলামাবাদ', 'নয়াদিল্লী', 'থিম্পু', 'জায়াবর্ধনপুর কোর্টে',  'মালে', 'কাঠমুন্ডু', 'কাবুল', 'নাইপিদাও', 'হ্যানয়', 'ব্যাংকক',
        'নমপেন', 'দিলি', 'জাকার্তা', 'কুয়ালালামপুর', 'রিয়াদ', 'তেহরান', 'বাগদাদ', 'সানা', 'জেরুজালেম', 'মাস্কট', 'দোহা', 'আম্মান',
        'আংকারা', 'দামেস্ক', 'পিয়ংইয়ং', 'সিউল', 'বেইজিং', 'টোকিও'
    )

    streets = (
        'জিগাতলা', 'নুতন রাস্তা', 'বেইলি রোড', '৭/A'
    )

    states = (
        'ঢাকা',
        'চট্টগ্রাম',
        'রাজশাহী',
        'খুলনা',
        'বরিশাল',
        'সিলেট',
        'রংপুর',
    )

    countries = (
        'বাংলাদেশে' , 'পাকিস্তান', 'ভারত', 'ভুটান', 'শ্রীলংকা', 'মালদ্বীপ', 'নেপাল', 'আফগানিস্তান',  'মায়ানমার', 'ভিয়েতনাম',
         'থাইল্যান্ড', 'কম্বোডিয়া', 'পূর্ব তিমুর', 'ইন্দোনেশিয়া', 'মালয়েশিয়া', 'সৌদি আরব', 'ইরান', 'ইরাক', 'ইয়েমেন', 'ইসরাইল',
          'ওমান',  'কাতার', 'জর্ডান', 'তুরস্ক', 'সিরিয়া', 'উত্তর কোরিয়া', 'দক্ষিন কোরিয়া', 'চীন', 'জাপান'
    )

    @classmethod
    def street_suffix_short(cls):
        return cls.random_element(cls.street_suffixes_short)

    @classmethod
    def street_suffix_long(cls):
        return cls.random_element(cls.street_suffixes_long)

    @classmethod
    def city_name(cls):
        return cls.random_element(cls.cities)

    @classmethod
    def street_name(cls):
        return cls.random_element(cls.streets)

    @classmethod
    def state(cls):
        return cls.random_element(cls.states)
