from src.model import scan_image

def main():
    prediction, prob = scan_image("https://media.cntraveler.com/photos/5eb18e42fc043ed5d9779733/16:9/w_960%2Cc_limit/BlackForest-Germany-GettyImages-147180370.jpg")
    print(f"Prediction: {prediction}, Probability: {prob:.2f}%")


if __name__ == "__main__":
    main()
