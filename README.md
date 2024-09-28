# training.py

Created by [**Robert (Bobby) Impastato**](https://github.com/bobbyimpastato) on 9/27/2024 for University of Illinois Urbana-Champaign code screening.

## Usage

To run, navigate to the project directory, then enter:

```bash
python training.py
```



You will be prompted on whether or not you would like to keep the default filename, fiscal year, training parameters, and expiration date from the original instructions. If you would like to keep these, simply respond with "Y" for all questions.

Upon exiting, three JSON files are exported:

  **completed_counts.json:** Contains the counts of how many people have completed each training.

  **people_completed_trainings.json:** Lists all people who completed specified trainings within the defined fiscal year.

  **expired_or_expiring_soon.json:** Details people with trainings that have expired or will expire soon based on the specified expiration date.
