import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Generative_AI_College_Students_960_genuine_Responses.csv")


pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", 1000)
print(df)

df.rename(
    columns={
        "Most_Frequently_Used_GenAI_Tool": "gen_ai_tool",
        "GenAI_Usage_Frequency": "usage_freq",
        "Primary_Purpose_of_GenAI": "main_purpose",
        "Time_Saving_Rating": "time_saving",
        "Trust_in_GenAI_Information": "trust_info",
        "AI_Information_Verification_Frequency": "verify_freq",
        "Experienced_AI_Hallucination": "hallucination",
        "Confidence_in_Identifying_AI_Hallucination": "hallucination_conf",
        "Biggest_GenAI_Concern": "main_concern",
        "Excessive_GenAI_Reduces_Independent_Thinking": "critical_thinking",
        "Overall_GenAI_Usefulness": "usefulness",
    },
    inplace=True,
)
# print(df)

print(df.shape)
print(df.info())
print(df.head())
print(df.describe(include="all"))
print(df.nunique())


df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()


text_columns = [
    "age_group",
    "year_of_study",
    "field_of_study",
    "gen_ai_tool",
    "usage_freq",
    "main_purpose",
    "time_saving",
    "trust_info",
    "verify_freq",
    "hallucination",
    "hallucination_conf",
    "main_concern",
    "critical_thinking",
    "usefulness",
]


for col in text_columns:
    df[col] = df[col].astype("string").str.strip().str.title()


print(df.head(1).T)


print(df.duplicated().sum())

print(df["main_purpose"].value_counts())

purpose_map = {
    "Understanding Concepts": "Academic",
    "Academic Assignments": "Academic",
    "Research": "Academic",
    "Exam Preparation": "Academic",
    "Coding/Programming": "Technical",
    "Writing/Grammar": "Productivity",
    "Personal Use": "Productivity",
    "Presentations": "Productivity",
    "Other": "Other",
}

df["primary_purpose"] = df["main_purpose"].map(purpose_map)
print("Unmapped Values:")
print(df.loc[df["primary_purpose"].isna(), "main_purpose"].unique())


print(df["primary_purpose"])
print(df["primary_purpose"].isnull().sum())
print(df["primary_purpose"].value_counts())


print(df["age_group"].value_counts())

age_intent_table = (
    df.groupby(["age_group", "primary_purpose"]).size().unstack(fill_value=0)
)
print(age_intent_table)


purpose_counts = df["primary_purpose"].value_counts(dropna=False)

summary_table = pd.DataFrame(
    {
        "Count": purpose_counts,
        "Percentage (%)": (purpose_counts / len(df) * 100).round(2),
    }
)

print(summary_table)


sns.set_theme(style="whitegrid")
plt.figure(figsize=(11, 6))

ax = age_intent_table.plot(kind="bar", colormap="viridis", width=0.8, ax=plt.gca())

for container in ax.containers:
    ax.bar_label(container, fmt="%d", padding=3, fontsize=9)

plt.title(
    "AI Primary Intent Distribution Across Age Groups", fontsize=14, fontweight="bold"
)

plt.xlabel("Age Groups", fontsize=12)
plt.ylabel("Number of Students", fontsize=12)

plt.xticks(rotation=0)
plt.legend(title="Primary Intent")

plt.grid(axis="y", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()

plt.savefig("age_vs_intent_chart.png", dpi=300, bbox_inches="tight")

plt.show()


intent_percentages = df["primary_purpose"].value_counts(normalize=True).mul(100)

plt.figure(figsize=(9, 5))

ax = intent_percentages.plot(kind="bar", color="#527c9e", width=0.6)

for container in ax.containers:
    ax.bar_label(
        container,
        labels=[f"{value:.1f}%" for value in container.datavalues],
        padding=3,
        fontsize=10,
    )

plt.title("Overall Primary Intent Distribution", fontsize=14, fontweight="bold")

plt.xlabel("Primary Intent", fontsize=12)
plt.ylabel("Percentage of Students (%)", fontsize=12)

plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.4)

ax.set_axisbelow(True)

plt.tight_layout()

plt.savefig("overall_intent_chart.png", dpi=300, bbox_inches="tight")

plt.show()

df.to_csv("Generative_AI_College_Students_960_genuine_Responses_v2.csv", index=False)
