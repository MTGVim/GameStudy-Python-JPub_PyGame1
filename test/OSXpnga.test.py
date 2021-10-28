# Fixes the issue when trying to render RBGAs that have 8bits of information in the alpha channel
# Turns your image into 8 bits on RGB and then 1 bit on the A channel
# This will render correctly
# See the example below for how to use

from PIL import Image


def flattenAlpha(img):
    alpha = img.split()[-1]  # Pull off the alpha layer
    ab = alpha.tobytes()  # Original 8-bit alpha

    checked = []  # Create a new array to store the cleaned up alpha layer bytes

    # Walk through all pixels and set them either to 0 for transparent or 255 for opaque fancy pants
    transparent = 50  # change to suit your tolerance for what is and is not transparent

    p = 0
    for pixel in range(0, len(ab)):
        if ab[pixel] < transparent:
            checked.append(0)  # Transparent
        else:
            checked.append(255)  # Opaque
        p += 1

    mask = Image.frombytes('L', img.size, bytes(checked))

    img.putalpha(mask)

    return img

# Run this as a test case.
# Assumes that you have a PNG named "CuriosityRover.png"
# that is an RGBA with varying levels of Alpha in the
# subdirectory assets from your working directory

if __name__ == "__main__":
    from PIL import ImageTk
    import tkinter as tk

    img = Image.open("./Assets/CuriosityRover.png")

    img = flattenAlpha(img)
    root = tk.Tk()

    photo = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(root, width=600, height=600, bg="red")

    canvas.create_image((300, 300), image=photo)
    canvas.grid(row=0, column=0)

    root.mainloop()