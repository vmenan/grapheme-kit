import re
import os 
import unicodedata


class Normalizer:
    """
    Handles Tamil-specific normalization, Unicode standardization (NFC),
    and grammatical validation rules (Nanool).
    """

    def normalize(self, text: str) -> str:
        """
        Main entry point for normalization.
        1. Applies Standard Unicode NFC normalization.
        2. Applies Tamil-specific character fixups.
        """
        # 1. Standard Unicode NFC Normalization (Canonical Composition)
        text = unicodedata.normalize('NFC', text)

        # 2. Tamil Specific Normalization
        text = self._char_fixup(text)

        return text

    def _char_fixup(self, word: str) -> str:
        # Tamil fixup_____________________________________________________________________________________________
        # 1. Standard normalization fixes
        word = word.replace('ோ', 'ோ')
        word = word.replace('ொ', 'ொ')
        word = word.replace('ா்', 'ர்')
        word = word.replace('ாி', 'ரி')

        # 2. Remove Zero Width Joiner/Non-Joiner
        word = word.replace('\u200C', '')

        # 3. Fix reverse vowel orders
        word = word.replace('ாெ', 'ொ')
        word = word.replace('ாே', 'ோ')

        # 4. Conditional 'ெ' + 'ள' -> 'ௌ'
        # Only if NOT followed by a vowel-like marker
        tamil_dependent_vowels = ['ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ', '்']
        vowels_pattern = '[' + ''.join(tamil_dependent_vowels) + ']'
        pattern = re.compile(r'ெள(?!' + vowels_pattern + ')')
        word = pattern.sub('ௌ', word)

        # Sinhala fixup________________________________________________________________________________________

        confusion_set={"ේා":"ෝ", "්ො":"ෝ", "්ාෙ":"ෝ", "ා්ෙ":"ෝ", "ාේ":"ෝ",'ේා':"ෝ",
                      "ෟෙ":"ෞ",
                       "ෙ‌ෙ":"'ෛ'",
                       "‌ො":"ො",
                       "්ෙ":"ේ",
                        "‌ෙ":"ෙ"
                       }
        for key,value in confusion_set.items():
          word=word.replace(key,value)


        return word

    def sandhi_remover(self, word: str) -> str:
        word = word.strip()
        sandhi_letters = {'க்','த்','ப்','ச்'}
        for x in sandhi_letters:
            p = re.compile(x + "$")
            if p.search(word):
                word = word[:-2]
        return word

    # --- Validation Logic (Preserved from original code) ---

    def check_starting_letter(self, word: str) -> bool:
        uyir=["அ","ஆ","இ","ஈ","உ","ஊ","எ","ஏ","ஐ","ஒ","ஓ","ஔ"]
        ka=["க","கா","கி","கீ","கு","கூ","ெக","ேக","ைக","ெகா","கோ","ெகள"]
        ca=["ச","சா","சி","சீ","சு","சூ","செ","சே","சை","சொ","சோ","சௌ"]
        tha=["த","தா","தி","தீ","து","தூ","தெ","தே","தை","தொ","தோ","தௌ"]
        na=["ந","நா","நி","நீ","நு","நூ","நெ","நே","நை","நொ","நோ","நௌ"]
        pa=["ப","பா","பி","பீ","பு","பூ","பெ","பே","பை","பொ","போ","பௌ"]
        ma=["ம","மா","மி","மீ","மு","மூ","மெ","மே","மை","மொ","மோ","மௌ"]
        va=["வ","வா","வி","வீ","வெ","வே","வை","வௌ"]
        ya=["ய","யா","யு","யூ","யோ","யௌ"]
        gna=["ஞ","ஞா","ஞெ","ஞொ"]

        letters = uyir + ka + ca + tha + na + pa + ma + va + ya + gna

        for x in letters:
            if word.startswith(x): # Optimized from regex match
                return True
        return False

    def check_ending_letter(self, word: str) -> bool:
        uyir_oreluthu_orumozhi=["ஆ","ஈ","ஊ","ஏ","ஐ","ஓ","ஒள"]
        uyir_a=["க","ங","ச","ஞ","ட","ண","த","ந","ப","ம","ய","ர","ழ","வ","ள","ல","ற","ன"]
        mei=["ஞ்","ண்","ந்","ம்","ன்","ய்","ர்","ல்","வ்","ழ்","ள்"]
        uyir_rest=["ா","ி","ீ","ு","ூ","ே","ை","ொ","ோ","ௌ"]

        # Note: Logic preserved, but if strict grapheme splitting is used later,
        # regex checking on raw unicode points might need adjustment.
        letters = uyir_a + uyir_rest + mei

        if len(word) == 1:
            return word in uyir_oreluthu_orumozhi
        else:
            for x in letters:
                p = re.compile(x + "$")
                if p.search(word):
                    return True
        return False

    # Placeholder for the massive CheckMeimmayakkam logic
    # I have kept the structure but omitted the full list definitions for brevity
    # in this view, but in your production file, paste the full function here.
    def check_meimmayakkam(self, word: str) -> bool:
        # ... Insert the full list logic from your snippet here ...
        # For now, returning True to assume valid
        return True