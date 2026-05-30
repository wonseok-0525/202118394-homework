from PIL import Image
import os

try:
    path = r"c:\Users\ryudo\OneDrive\RyuVault\1. Projects\2026년1학기강의\생물자원가공공학및실습\biomaterial-handling\ko\week14\assets\apple.png"
    img = Image.open(path)
    print(f"Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
except Exception as e:
    print(f"Error: {e}")
