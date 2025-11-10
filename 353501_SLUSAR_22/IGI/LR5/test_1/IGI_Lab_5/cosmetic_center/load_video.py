#!/usr/bin/env python
import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_center.settings')
django.setup()

from clinic.models import CompanyInfo
import shutil

# Path to your video file
video_path = r"C:\Users\Anzherus\Desktop\IGI\353501_SLUSAR_22\353501_SLUSAR_22\IGI\LR5\test_1\IGI_Lab_5\cosmetic_center\media\company\Видео ролик для косметолога, процедура микронидлинг.mp4"

def load_video():
    """Loads your video for the company"""
    
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        print("Make sure the file exists at the specified path.")
        return False
    
    print(f"📁 Found file: {os.path.basename(video_path)}")
    
    try:
        # Create videos directory if it doesn't exist
        videos_dir = 'media/company/videos'
        os.makedirs(videos_dir, exist_ok=True)
        
        # Get company information
        company_info = CompanyInfo.objects.filter(name="Косметологический Центр «Эстетика»").first()
        
        if not company_info:
            print("❌ Company information not found. Please run create_company_info.py first")
            return False
        
        # Copy video file with Russian name to standardized filename
        video_filename = "company_video.mp4"
        dest_path = os.path.join(videos_dir, video_filename)
        
        print(f"📋 Copying video to: {dest_path}")
        shutil.copy2(video_path, dest_path)
        
        # Update company information
        relative_path = f'company/videos/{video_filename}'
        company_info.video_file = relative_path
        company_info.video_url = ''  # Clear URL to use local file
        company_info.save()
        
        print("✅ Video successfully uploaded!")
        print(f"🎥 Video file: {dest_path}")
        print(f"🔗 Relative path: {relative_path}")
        print("📺 Video will now be displayed on the 'About Us' page")
        print("\n🌟 Open the website and go to the 'About Us' page to see your video!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading video: {str(e)}")
        return False

if __name__ == '__main__':
    print("=== Company Video Upload ===")
    print(f"📁 Video path: {video_path}")
    print()
    
    load_video()
