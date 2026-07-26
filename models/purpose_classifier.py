import pandas as pd

# Define purpose categories with keywords
PURPOSE_CATEGORIES = {
    "Official Work": [
        "meeting", "office", "official", "inspection", "audit",
        "documentation", "training", "conference"
    ],
    "Employee Visit": [
        "employee", "staff", "joining", "duty", "work"
    ],
    "Contractor": [
        "contractor", "maintenance", "repair", "installation",
        "vendor", "service"
    ],
    "Material Delivery": [
        "delivery", "material", "goods", "supply", "dispatch",
        "courier", "shipment"
    ],
    "Family Visit": [
        "family", "relative", "quarters", "personal visit"
    ],
    "Interview": [
        "interview", "recruitment", "candidate", "hr"
    ],
    "Medical": [
        "medical", "hospital", "health", "checkup", "emergency"
    ],
    "Other": []
}


def classify_purpose(purpose):
    """
    Classify a single purpose into a predefined category.
    """
    purpose = str(purpose).lower()

    for category, keywords in PURPOSE_CATEGORIES.items():
        for keyword in keywords:
            if keyword in purpose:
                return category

    return "Other"


def classify_dataframe(df):
    """
    Add a new column 'Purpose_Category'
    """
    df = df.copy()
    df["Purpose_Category"] = df["Purpose of Visit"].apply(classify_purpose)
    return df


def purpose_summary(df):
    """
    Return count of each purpose category.
    """
    classified_df = classify_dataframe(df)

    summary = (
        classified_df["Purpose_Category"]
        .value_counts()
        .reset_index()
    )

    summary.columns = ["Category", "Count"]

    return summary