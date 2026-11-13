import pandas as pd
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_FILE = os.path.join(
    BASE_DIR,
    "processed_data",
    "food_waste_processed.csv"
)


def generate_insight(city):

    df = pd.read_csv(
        DATA_FILE
    )

    city_df = df[
        df["City"]
        .astype(str)
        .str.lower()
        == city.lower()
    ]

    if city_df.empty:

        return {
            "level": "Unknown",
            "insight": "No data available.",
            "recommendation": "Upload a valid dataset."
        }

    total_prepared = (
        city_df["Prepared_kg"]
        .sum()
    )

    total_waste = (
        city_df["Waste_kg"]
        .sum()
    )

    waste_percentage = (

        total_waste
        /
        total_prepared
        * 100

        if total_prepared > 0

        else 0
    )

    food_waste = (
        city_df
        .groupby("Food")["Waste_kg"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    highest_food = (
        food_waste.index[0]
    )

    highest_food_waste = (
        food_waste.iloc[0]
    )

    if waste_percentage >= 20:

        level = "High"

        insight = (
            f"High food waste detected in "
            f"{city}. {waste_percentage:.2f}% "
            f"of prepared food was wasted."
        )

        recommendation = (
            f"{highest_food} has the highest "
            f"waste contribution. Consider "
            f"reducing preparation quantity "
            f"and improving demand planning."
        )

    elif waste_percentage >= 10:

        level = "Medium"

        insight = (
            f"Moderate food waste detected "
            f"in {city}. The waste percentage "
            f"is {waste_percentage:.2f}%."
        )

        recommendation = (
            f"Review consumption patterns "
            f"for {highest_food} and adjust "
            f"future preparation quantities."
        )

    else:

        level = "Low"

        insight = (
            f"Food waste in {city} is "
            f"{waste_percentage:.2f}%."
        )

        recommendation = (
            "Continue monitoring preparation "
            "and consumption patterns."
        )

    return {

        "city": city,

        "level": level,

        "waste_percentage":
            round(
                waste_percentage,
                2
            ),

        "highest_food":
            highest_food,

        "highest_food_waste":
            round(
                highest_food_waste,
                2
            ),

        "insight": insight,

        "recommendation":
            recommendation
    }


if __name__ == "__main__":

    result = generate_insight(
        "Hyderabad"
    )

    print(result)