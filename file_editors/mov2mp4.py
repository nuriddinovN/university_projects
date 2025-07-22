import subprocess
import os
import sys

def convert_mov_to_mp4(input_path, output_path=None, quality='medium'):
    """
    Convert MOV video file to MP4 format using FFmpeg
    
    Args:
        input_path (str): Path to input MOV file
        output_path (str): Path for output MP4 file (optional)
        quality (str): Conversion quality - 'high', 'medium', 'low'
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found!")
        return False
    
    # Generate output path if not provided
    if output_path is None:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_converted.mp4"
    
    # Quality settings
    quality_settings = {
        'high': ['-crf', '18'],      # High quality, larger file
        'medium': ['-crf', '23'],    # Balanced quality/size
        'low': ['-crf', '28']        # Lower quality, smaller file
    }
    
    # Build FFmpeg command
    cmd = [
        'ffmpeg',
        '-i', input_path,           # Input file
        '-c:v', 'libx264',          # Video codec
        '-c:a', 'aac',              # Audio codec
        '-movflags', '+faststart',   # Optimize for web streaming
        '-y',                       # Overwrite output file
    ]
    
    # Add quality settings
    if quality in quality_settings:
        cmd.extend(quality_settings[quality])
    else:
        cmd.extend(quality_settings['medium'])
    
    cmd.append(output_path)         # Output file
    
    try:
        print(f"Converting {input_path} to {output_path}...")
        print(f"Quality: {quality}")
        
        # Run FFmpeg conversion
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Conversion successful!")
            print(f"Output saved to: {output_path}")
            
            # Show file sizes
            input_size = os.path.getsize(input_path) / (1024*1024)
            output_size = os.path.getsize(output_path) / (1024*1024)
            print(f"Original size: {input_size:.1f} MB")
            print(f"Converted size: {output_size:.1f} MB")
            
            return True
        else:
            print(f"Error during conversion:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("Error: FFmpeg not found! Please install FFmpeg first.")
        print("Download from: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def batch_convert(input_folder, output_folder=None, quality='medium'):
    """
    Convert all MOV files in a folder to MP4
    
    Args:
        input_folder (str): Folder containing MOV files
        output_folder (str): Output folder (optional)
        quality (str): Conversion quality
    """
    
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' not found!")
        return
    
    # Create output folder if specified
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Find all MOV files
    mov_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mov')]
    
    if not mov_files:
        print("No MOV files found in the specified folder.")
        return
    
    print(f"Found {len(mov_files)} MOV files to convert...")
    
    successful = 0
    for mov_file in mov_files:
        input_path = os.path.join(input_folder, mov_file)
        
        if output_folder:
            output_file = os.path.splitext(mov_file)[0] + '.mp4'
            output_path = os.path.join(output_folder, output_file)
        else:
            output_path = None
        
        if convert_mov_to_mp4(input_path, output_path, quality):
            successful += 1
        
        print("-" * 50)
    
    print(f"Batch conversion complete: {successful}/{len(mov_files)} files converted successfully.")

# =============================================================================
# USAGE EXAMPLES - Modify the paths below for your specific videos
# =============================================================================

if __name__ == "__main__":
    
    # Example 1: Convert single video
    # Specify your video path here:
    video_path = "/var/home/noor/IMG_3621.MOV"
    
    # Optional: specify output path
    output_path = "/var/home/noor/output.mp4"
    
    # Convert single file (uncomment to use)
    # convert_mov_to_mp4(video_path, output_path, quality='medium')
    
    # Example 2: Convert with automatic output naming
    # convert_mov_to_mp4(video_path, quality='high')
    
    # Example 3: Batch convert all MOV files in a folder
    # input_folder = "/path/to/your/iphone/videos/"
    # output_folder = "/path/to/converted/videos/"
    # batch_convert(input_folder, output_folder, quality='medium')
    
    # Example 4: Interactive mode
    print("MOV to MP4 Converter")
    print("=" * 30)
    
    while True:
        print("\nOptions:")
        print("1. Convert single file")
        print("2. Batch convert folder")
        print("3. Exit")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            input_path = input("Enter MOV file path: ").strip()
            quality = input("Enter quality (high/medium/low) [medium]: ").strip() or 'medium'
            convert_mov_to_mp4(input_path, quality=quality)
            
        elif choice == '2':
            folder_path = input("Enter folder path containing MOV files: ").strip()
            quality = input("Enter quality (high/medium/low) [medium]: ").strip() or 'medium'
            batch_convert(folder_path, quality=quality)
            
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
