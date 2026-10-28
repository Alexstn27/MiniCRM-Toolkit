import pandas as pd
import unicodedata
from core.constants import (
    EMAIL_COLUMN,
    NAME_COLUMN,
    PHONE_COLUMN,
    WORKPLACE_COLUMN,
    CITY_COLUMN,
    NAME_SCORE,
    PHONE_SCORE,
    WORKPLACE_SCORE,
    CITY_SCORE
)
from core.helpers import (
    load_excel,
    save_excel
)

class DuplicateRemoverModule:

    def load_excel(self, file_path):

        return load_excel(file_path)


    def validate_columns(self, dataframe):

        required_columns = [
            EMAIL_COLUMN
        ]

        for column in required_columns:

            if column not in dataframe.columns:
                return False

        return True


    def remove_duplicates(self, dataframe):

        original_count = len(dataframe)

        dataframe_with_email = dataframe[
            dataframe[EMAIL_COLUMN].notna()
        ].copy()

        dataframe_without_email = dataframe[
            dataframe[EMAIL_COLUMN].isna()
        ].copy()

        dataframe_with_email = dataframe_with_email.drop_duplicates(
            subset=[EMAIL_COLUMN],
            keep="first"
        )

        dataframe = pd.concat(
            [
                dataframe_with_email,
                dataframe_without_email
            ],
            ignore_index=True
        )

        removed_count = original_count - len(dataframe)

        return dataframe, removed_count

    def calculate_duplicate_score(
            self,
            row1,
            row2,
            dataframe
        ):

            earned_points = 0
            possible_points = 0

            # Nume
            possible_points += NAME_SCORE

            if row1[NAME_COLUMN] == row2[NAME_COLUMN]:
                earned_points += NAME_SCORE

            # Telefon
            if (
                PHONE_COLUMN in dataframe.columns
                and not pd.isna(row1[PHONE_COLUMN])
                and not pd.isna(row2[PHONE_COLUMN])
            ):

                possible_points += PHONE_SCORE

                if row1[PHONE_COLUMN] == row2[PHONE_COLUMN]:
                    earned_points += PHONE_SCORE

            # Loc de muncă
            if (
                WORKPLACE_COLUMN in dataframe.columns
                and not pd.isna(row1[WORKPLACE_COLUMN])
                and not pd.isna(row2[WORKPLACE_COLUMN])
            ):

                possible_points += WORKPLACE_SCORE

                if row1[WORKPLACE_COLUMN] == row2[WORKPLACE_COLUMN]:
                    earned_points += WORKPLACE_SCORE

            # Oraș
            if (
                CITY_COLUMN in dataframe.columns
                and not pd.isna(row1[CITY_COLUMN])
                and not pd.isna(row2[CITY_COLUMN])
            ):

                possible_points += CITY_SCORE

                if row1[CITY_COLUMN] == row2[CITY_COLUMN]:
                    earned_points += CITY_SCORE

            if possible_points == 0:
                return 0

            percentage = round(
                earned_points / possible_points * 100
            )

            return percentage

    def get_score_stars(self, score):

        if score >= 90:
            return "★★★★★"

        elif score >= 75:
            return "★★★★☆"

        elif score >= 60:
            return "★★★☆☆"

        elif score >= 40:
            return "★★☆☆☆"

        else:
            return "★☆☆☆☆"

    def find_possible_duplicates_without_email(self, dataframe):

        dataframe_without_email = dataframe[
            dataframe[EMAIL_COLUMN].isna()
        ].copy()

        duplicate_rows = dataframe_without_email[
            dataframe_without_email.duplicated(
                subset=[NAME_COLUMN],
                keep=False
            )
        ]

        results = []

        processed_names = []

        for name in duplicate_rows[NAME_COLUMN].unique():

            if name in processed_names:
                continue

            people = duplicate_rows[
                duplicate_rows[NAME_COLUMN] == name
            ]

            if len(people) < 2:
                continue

            row1 = people.iloc[0]
            row2 = people.iloc[1]

            score = self.calculate_duplicate_score(
                row1,
                row2,
                dataframe
            )

            results.append(
                {
                    "name": name,
                    "score": score
                }
            )

            processed_names.append(name)

        return results
    
    def save_excel(self, dataframe):

        return save_excel(
            dataframe,
            "MiniCRM - Participanți fără duplicate"
        )


def _compare_normalize(value):
    """Normalizează textul pentru comparări fără diferențe de litere mari, spații sau diacritice."""
    if value is None or pd.isna(value):
        return ""

    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(
        character
        for character in text
        if not unicodedata.combining(character)
    )

    return " ".join(text.casefold().strip().split())


def _compare_find_column(dataframe, aliases):
    """Găsește o coloană după numele ei, ignorând diferențele de scriere."""
    normalized_aliases = {
        _compare_normalize(alias).replace(" ", "").replace(":", "")
        for alias in aliases
    }

    for column in dataframe.columns:
        normalized_column = (
            _compare_normalize(column)
            .replace(" ", "")
            .replace(":", "")
        )

        if normalized_column in normalized_aliases:
            return column

    return None


def _compare_get_columns(dataframe):
    """Identifică emailul, numele și prenumele dintr-un export Excel."""
    email_column = _compare_find_column(
        dataframe,
        [
            "Persoana1: Email",
            "Email",
            "E-mail",
            "Mail",
            "Email participant",
        ],
    )

    surname_column = _compare_find_column(
        dataframe,
        [
            "Persoana1: Nume",
            "Nume",
            "Surname",
            "Last Name",
        ],
    )

    first_name_column = _compare_find_column(
        dataframe,
        [
            "Persoana1: Prenume",
            "Prenume",
            "First Name",
            "Given Name",
        ],
    )

    full_name_column = _compare_find_column(
        dataframe,
        [
            "Contact: Nume",
            "Participant: Nume",
            "Nume și prenume",
            "Nume si prenume",
            "Nume prenume",
            "Full Name",
            "Name",
        ],
    )

    if not email_column and not (
        full_name_column or surname_column or first_name_column
    ):
        raise ValueError(
            "Nu am găsit coloanele de email sau nume în fișier."
        )

    return (
        email_column,
        surname_column,
        first_name_column,
        full_name_column,
    )


def _compare_get_email(row, email_column):
    if not email_column:
        return ""

    return _compare_normalize(row[email_column])


def _compare_get_name(
    row,
    surname_column,
    first_name_column,
    full_name_column,
):
    surname = (
        _compare_normalize(row[surname_column])
        if surname_column
        else ""
    )

    first_name = (
        _compare_normalize(row[first_name_column])
        if first_name_column
        else ""
    )

    if surname or first_name:
        return f"{surname} {first_name}".strip()

    if full_name_column:
        return _compare_normalize(row[full_name_column])

    return ""


def compare_and_filter_files(main_file, comparison_file):
    """
    Compară lista principală cu lista de comparație.
    Salvează participanții rămași și cazurile de verificat
    în două sheet-uri separate.
    """
    main_df = load_excel(main_file)
    comparison_df = load_excel(comparison_file)

    main_columns = _compare_get_columns(main_df)
    comparison_columns = _compare_get_columns(comparison_df)

    (
        main_email_col,
        main_surname_col,
        main_first_col,
        main_full_name_col,
    ) = main_columns

    (
        comp_email_col,
        comp_surname_col,
        comp_first_col,
        comp_full_name_col,
    ) = comparison_columns

    def display_value(row, column):
        if not column:
            return ""

        value = row[column]

        if value is None or pd.isna(value):
            return ""

        return str(value).strip()

    def display_name(
        row,
        surname_column,
        first_name_column,
        full_name_column,
    ):
        if surname_column or first_name_column:
            surname = display_value(row, surname_column)
            first_name = display_value(row, first_name_column)

            return " ".join(
                part for part in (surname, first_name) if part
            )

        return display_value(row, full_name_column)

    review_columns = [
        "Motiv verificare",
        "Nume lista principala",
        "Email lista principala",
        "Nume lista achitati",
        "Email lista achitati",
    ]

    review_records = []
    review_keys = set()

    def add_review(
        reason,
        main_name,
        main_email,
        comparison_person,
    ):
        record = {
            "Motiv verificare": reason,
            "Nume lista principala": main_name,
            "Email lista principala": main_email,
            "Nume lista achitati": comparison_person["display_name"],
            "Email lista achitati": comparison_person["display_email"],
        }

        key = tuple(record[column] for column in review_columns)

        if key not in review_keys:
            review_keys.add(key)
            review_records.append(record)

    # Indexăm persoanele din lista de comparație după email și nume.
    comparison_by_email = {}
    comparison_by_name = {}

    for _, row in comparison_df.iterrows():
        email = _compare_get_email(row, comp_email_col)

        name = _compare_get_name(
            row,
            comp_surname_col,
            comp_first_col,
            comp_full_name_col,
        )

        person = {
            "normalized_name": name,
            "normalized_email": email,
            "display_name": display_name(
                row,
                comp_surname_col,
                comp_first_col,
                comp_full_name_col,
            ),
            "display_email": display_value(row, comp_email_col),
        }

        if email:
            comparison_by_email.setdefault(email, []).append(person)

        if name:
            comparison_by_name.setdefault(name, []).append(person)

    rows_to_keep = []
    removed_by_email = 0
    removed_by_name = 0

    for index, row in main_df.iterrows():
        email = _compare_get_email(row, main_email_col)

        name = _compare_get_name(
            row,
            main_surname_col,
            main_first_col,
            main_full_name_col,
        )

        main_display_name = display_name(
            row,
            main_surname_col,
            main_first_col,
            main_full_name_col,
        )

        main_display_email = display_value(row, main_email_col)

        matched = False

        # 1. Potrivire după email.
        if email and email in comparison_by_email:
            matched = True
            removed_by_email += 1

            # Email comun, dar nume diferit sau lipsă:
            # persoana se elimină după email, dar cazul se verifică.
            for person in comparison_by_email[email]:
                if name != person["normalized_name"]:
                    add_review(
                        "Email comun, nume diferit sau lipsa",
                        main_display_name,
                        main_display_email,
                        person,
                    )

        # 2. Același nume, dar email diferit sau lipsă.
        elif name and name in comparison_by_name:
            candidates = comparison_by_name[name]

            non_empty_emails = {
                person["normalized_email"]
                for person in candidates
                if person["normalized_email"]
            }

            # Dacă emailurile lipsesc din ambele liste,
            # păstrăm regula existentă de potrivire după nume.
            if not email and not non_empty_emails:
                matched = True
                removed_by_name += 1

            else:
                # Nu eliminăm automat o persoană când emailurile
                # nu confirmă că este aceeași persoană.
                for person in candidates:
                    if email != person["normalized_email"]:
                        add_review(
                            "Nume comun, email diferit sau lipsa",
                            main_display_name,
                            main_display_email,
                            person,
                        )

        if not matched:
            rows_to_keep.append(index)

    # Păstrăm toate coloanele și ordinea din lista principală.
    filtered_df = main_df.loc[rows_to_keep].copy()

    # Salvăm fișierul folosind mecanismul existent al aplicației.
    output_path = save_excel(
        filtered_df,
        "Participanti ramasi dupa comparare",
    )

    # Creăm al doilea sheet pentru verificare manuală.
    review_df = pd.DataFrame(
        review_records,
        columns=review_columns,
    )

    # Scriem ambele sheet-uri în fișierul rezultat.
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        filtered_df.to_excel(
            writer,
            sheet_name="Participanti ramasi",
            index=False,
        )

        review_df.to_excel(
            writer,
            sheet_name="De verificat",
            index=False,
        )

    return {
        "main_count": len(main_df),
        "comparison_count": len(comparison_df),
        "removed_by_email": removed_by_email,
        "removed_by_name": removed_by_name,
        "removed_count": removed_by_email + removed_by_name,
        "remaining_count": len(filtered_df),
        "possible_conflicts": len(review_records),
        "review_records": review_records,
        "output_path": output_path,
    }
