import os
import pandas as pd
from InquirerPy import prompt, inquirer, exceptions
from colorama import Fore, Back, Style
import plotext as plt
import sys

sys.tracebacklimit = 0


def get_csv() -> pd.DataFrame:
    """Returns the arguments necessary for label_data

    Returns:
        data (pd.DataFrame): The csv file as a pandas dataframe.
        feature_column (str): The feature to be labeled.
        labels (list): The list of labels to use when labeling the feature.
    """

    os.system("cls")

    try:
        selected_file = inquirer.select(
            message="Select file: ",
            choices=[f for f in os.listdir(".") if f.endswith(".csv")],
        ).execute()
    except exceptions.InvalidArgument:
        raise FileNotFoundError(
            Fore.RED + os.getcwd() + " should have at least one csv file." + Fore.RESET
        )

    data = pd.read_csv(f"./{selected_file}")
    feature_column = inquirer.select(
        message=f"Select column to label {selected_file} - (Rows: {data.shape[0]}, Columns: {data.shape[1]}):",
        choices=[
            f"{column} → ({data[column].isnull().sum()})" for column in data.columns
        ],
    ).execute()

    labels = prompt(
        {
            "type": "input",
            "message": "Add labels separated by a space: ",
            "name": "labels",
        }
    )["labels"].split(" ")

    return data, feature_column.split("→")[0].strip(), labels


def label_data(data: pd.DataFrame, feature: str, labels: list()) -> pd.DataFrame:
    """Label the csv file."""

    count = data.shape[0]

    if count == 0:
        raise Exception(
            f"{Fore.RED + feature} should have at least one row to be labeled."
            + Fore.RESET
        )

    labeled_data = {}
    skipped = 0
    os.system("cls")
    for idx, text in enumerate(data[feature]):
        print(
            Style.BRIGHT
            + Fore.LIGHTGREEN_EX
            + f"> Remaining {feature}s to be labeled: {count} - Skipped: {skipped} \n"
        )
        response = inquirer.select(
            message=text,
            choices=labels + ["Skip"],
        ).execute()

        if response == "Skip":
            skipped += 1
            response = ""

        labeled_data[idx] = {f"{feature}": text, "label": response}

        count = count - 1
        os.system("cls")

    data = pd.DataFrame(labeled_data).T
    data.to_csv(f"{feature}_labeled.csv", index=False)
    print("====== Percentage of Label ======")
    print(
        data["label"].value_counts(normalize=True).mul(100).round(1).astype(str) + "%"
    )
    plt.simple_bar(
        data["label"].value_counts().index.to_list(),
        data["label"].value_counts().to_list(),
        title="Distribution of Labels",
    )
    plt.show()

    print(f"Saved labeled data to {feature}_labeled.csv.")


def cli():

    os.system("cls")
    df, feature, labels = get_csv()
    label_data(df, feature, labels)


if __name__ == "__main__":
    cli()
