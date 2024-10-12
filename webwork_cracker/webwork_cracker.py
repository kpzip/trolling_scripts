import json
import urllib.parse
import requests
import re

# load cfg
with open("config.json", 'r') as file:
    cfg = json.load(file)

run_formatter = cfg["run_formatter"]

if run_formatter:
    import form_data_formatter
    form_data_formatter.run_formatter()

use_formatter_output = cfg["use_formatter_output"]

form_data = None

if use_formatter_output:
    with open("formatter_output.json", 'r') as formatter_out:
        form_data = json.load(formatter_out)
else:
    form_data = cfg["form_data"]

encoded = urllib.parse.urlencode(form_data)
# print(encoded)

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

url = cfg["initial_url"]

problem_id = cfg["problem_num"]
effective_user = cfg["effective_usr_urlencoded"]

post_url = url + problem_id
problem_url = post_url + effective_user

minimums = cfg["minimums"]
maximums = cfg["maximums"]
step = cfg["step"]


def get_form_inputs(html: str):

    # We love regular expressions
    forms = re.findall("<form.*?>.*?</form>", html, flags=re.DOTALL)
    problem_form = None
    for f in forms:
        if re.search("name=\"problemMainForm\"", f) is not None:
            problem_form = f
            break

    elements = re.findall("<input.*?>", problem_form)
    # print(elements)
    default_answers = {}
    free_answers = []
    for e in elements:
        id_search = re.search("name=\".*?\"", e)
        if id_search is not None:
            input_id = id_search.group().split('"')[1]
            value_search = re.search("value=\".*?\"", e)
            if value_search is not None and not input_id.startswith("AnSwEr") and not input_id.startswith("MaTrIx_AnSwEr"):
                value = value_search.group().split('"')[1]
                default_answers[input_id] = value
            else:
                free_answers.append(input_id)
    return default_answers, free_answers


def main():
    session = requests.Session()

    response = session.post(url, data=encoded, headers=headers)
    # print(response.text)

    authentication_worked = "Please enter your username and password for " not in response.text and "Not logged in." not in response.text
    if authentication_worked:
        problem_html = session.get(problem_url)
        # print(problem_html.text)
        fixed_form_elements, free_form_elements = get_form_inputs(problem_html.text)
        free_element_values = {}

        for i in range(len(free_form_elements)):
            e = free_form_elements[i]
            free_element_values[e] = minimums[i]

        running = True
        while running:

            data = fixed_form_elements
            data.update(free_element_values)
            for k, v in free_element_values.items():
                data["MaThQuIlL_" + k] = v

            submission_data = urllib.parse.urlencode(fixed_form_elements)
            resp = session.post(post_url, data=submission_data, headers=headers)
            fixed_form_elements, _ = get_form_inputs(resp.text)
            print(f"submitted answers: {free_element_values}")

            incorrect = "incorrect" in resp.text
            # print(incorrect)

            if not incorrect:
                if "correct" in resp.text:
                    print(f"Correct answer found: {free_element_values}")
                else:
                    print("error, session likely expired")
                break

            for i in range(len(free_form_elements)):
                e = free_form_elements[i]
                if free_element_values[e] > maximums[i]:
                    free_element_values[e] = minimums[i]
                    if e == free_form_elements[-1]:
                        running = False
                else:
                    free_element_values[e] += step
                    break
    else:
        print("Authentication Failed.")


if __name__ == "__main__":
    main()
