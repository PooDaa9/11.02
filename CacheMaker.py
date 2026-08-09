#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CacheMaker.py - أداة إنشاء ملفات cache.manifest تلقائياً
الإصدار: 2.0
"""

import os
import time
import json
from datetime import datetime

class CacheMaker:
    def __init__(self):
        self.files = []
        self.network = ['*']
        self.fallback = {}
        self.version = "1.0"
        self.comment = "ملف الكاش - تم إنشاؤه بواسطة CacheMaker"
    
    def add_file(self, file_path):
        """إضافة ملف فردي"""
        if file_path not in self.files:
            self.files.append(file_path)
    
    def add_files(self, file_list):
        """إضافة قائمة ملفات"""
        for file in file_list:
            self.add_file(file)
    
    def add_folder(self, folder_path, extension=None):
        """إضافة مجلد بالكامل مع إمكانية تحديد امتداد"""
        if not os.path.exists(folder_path):
            print(f"⚠️ تحذير: المجلد {folder_path} غير موجود")
            return
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if extension is None or file.endswith(extension):
                    full_path = os.path.join(root, file)
                    # تحويل المسار لنظام Unix
                    full_path = full_path.replace('\\', '/')
                    self.add_file(full_path)
    
    def set_network(self, network_list):
        """تحديد قائمة الشبكة"""
        self.network = network_list
    
    def set_fallback(self, fallback_dict):
        """تحديد صفحة الفال باك"""
        self.fallback = fallback_dict
    
    def set_version(self, version):
        """تحديد رقم الإصدار"""
        self.version = version
    
    def set_comment(self, comment):
        """إضافة تعليق"""
        self.comment = comment
    
    def remove_file(self, file_path):
        """حذف ملف من القائمة"""
        if file_path in self.files:
            self.files.remove(file_path)
    
    def clear_files(self):
        """مسح قائمة الملفات"""
        self.files = []
    
    def get_file_count(self):
        """عدد الملفات"""
        return len(self.files)
    
    def check_files_exist(self):
        """التحقق من وجود الملفات"""
        missing = []
        for file in self.files:
            if not os.path.exists(file):
                missing.append(file)
        return missing
    
    def generate(self, output_file='cache.manifest'):
        """إنشاء ملف الكاش"""
        # التحقق من وجود الملفات
        missing = self.check_files_exist()
        if missing:
            print(f"⚠️ تحذير: {len(missing)} ملف غير موجود:")
            for m in missing[:10]:  # عرض أول 10 ملفات فقط
                print(f"   - {m}")
            if len(missing) > 10:
                print(f"   ... و {len(missing)-10} ملف آخر")
        
        # كتابة الملف
        with open(output_file, 'w', encoding='utf-8') as f:
            # الرأس
            f.write('CACHE MANIFEST\n')
            f.write(f'# {self.comment}\n')
            f.write(f'# الإصدار: {self.version}\n')
            f.write(f'# تاريخ الإنشاء: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'# عدد الملفات: {len(self.files)}\n\n')
            
            # قسم CACHE
            if self.files:
                f.write('# ===== ملفات الكاش =====\n')
                f.write('CACHE:\n')
                for file in sorted(self.files):  # ترتيب الملفات
                    f.write(f'{file}\n')
                f.write('\n')
            
            # قسم NETWORK
            if self.network:
                f.write('# ===== السماح بالشبكة =====\n')
                f.write('NETWORK:\n')
                for net in self.network:
                    f.write(f'{net}\n')
                f.write('\n')
            
            # قسم FALLBACK
            if self.fallback:
                f.write('# ===== صفحات بديلة =====\n')
                f.write('FALLBACK:\n')
                for key, value in self.fallback.items():
                    f.write(f'{key} {value}\n')
        
        print(f'\n✅ تم إنشاء {output_file} بنجاح!')
        print(f'📦 عدد الملفات: {len(self.files)}')
        if missing:
            print(f'⚠️ ملفات مفقودة: {len(missing)}')
        return True


def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🚀 CacheMaker - أداة إنشاء ملفات الكاش")
    print("=" * 60)
    
    # إنشاء الكاش
    cache = CacheMaker()
    cache.set_version('2.0')
    cache.set_comment('ملف الكاش لبودة بلايستيشن - PS4 Jailbreak')
    
    # ===== إضافة الملفات =====
    print("\n📂 جاري إضافة الملفات...")
    
    # 1. الملفات الأساسية
    basic_files = [
        'index.html',
        'includes/cat.jpg',
        'includes/script.js',
        'includes/style.css',
    ]
    cache.add_files(basic_files)
    print(f"   ✅ أضيف {len(basic_files)} ملف أساسي")
    
    # 2. ملفات الجافاسكريبت
    js_files = [
        'src/main.js',
        'src/lapse.js',
        'src/loader.js',
        'src/misc.js',
        'src/netctrl.js',
        'src/worker.js',
        'src/workers.js',
    ]
    cache.add_files(js_files)
    print(f"   ✅ أضيف {len(js_files)} ملف جافاسكريبت")
    
    # 3. ملفات PS4
    ps4_files = [
        'src/ps4/constants.js',
        'src/ps4/kernel.js',
        'src/ps4/userland.js',
        'src/payload.bin',
    ]
    cache.add_files(ps4_files)
    print(f"   ✅ أضيف {len(ps4_files)} ملف PS4")
    
    # 4. باتشات PS4 (جميع الإصدارات)
    patches = [
        '600', '620', '650', '670', '700', '750',
        '800', '850', '900', '903', '950',
        '1000', '1050', '1100', '1102'
    ]
    
    patch_files = []
    for patch in patches:
        patch_files.append(f'src/ps4/patches/{patch}.bin')
    
    cache.add_files(patch_files)
    print(f"   ✅ أضيف {len(patch_files)} باتش PS4")
    
    # ===== إعدادات إضافية =====
    cache.set_network(['*'])
    cache.set_fallback({'/': '/index.html'})
    
    # ===== عرض الإحصائيات =====
    print("\n📊 إحصائيات:")
    print(f"   📦 إجمالي الملفات: {cache.get_file_count()}")
    
    # التحقق من وجود الملفات
    missing = cache.check_files_exist()
    if missing:
        print(f"   ⚠️ ملفات مفقودة: {len(missing)}")
        print("\n📋 الملفات المفقودة:")
        for m in missing:
            print(f"   - {m}")
    else:
        print("   ✅ جميع الملفات موجودة")
    
    # ===== إنشاء الملف =====
    print("\n🔄 جاري إنشاء cache.manifest...")
    cache.generate('cache.manifest')
    
    # ===== حفظ نسخة احتياطية =====
    backup_file = f'cache.manifest.backup.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    cache.generate(backup_file)
    print(f"📦 نسخة احتياطية: {backup_file}")
    
    print("\n" + "=" * 60)
    print("✅ تم الانتهاء بنجاح!")
    print("=" * 60)


if __name__ == '__main__':
    main()