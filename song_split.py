import sys, os

def song_split(song):
    filename = song[0]

    model_directory = "/workspaces/ominous-space-journey-7v475wgpwrxj3pxgg/models" 
    os.system(f"""
        docker run --rm \
              -v $(pwd)/input:/input \
              -v $(pwd)/outputs:/output \
              -v {model_directory}:/model \
              -e MODEL_PATH=/model \
              deezer/spleeter:3.8-4stems \
              separate -o /output -p spleeter:4stems /input/{filename}
    """)
def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        song_split(filename)
    else:
        print("Please provide a song filename as a command-line argument.")

if __name__ == "__main__":
    main()
