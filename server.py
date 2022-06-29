from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd


# data table format
df = pd.read_csv("data1.csv")
columns_strip_dict = {}
df.set_index("inputs", inplace=True)
for column in df:
    columns_strip_dict[column] = lambda x: x.strip("[]").split(", ")
df = pd.read_csv("data1.csv", converters=columns_strip_dict)
df.set_index("inputs", inplace=True)


# tools table format
df_tools = pd.read_csv("tools1.csv")
df_tools.set_index("name", inplace=True)
only_tools_dict = df_tools.to_dict()


tools_list = []
for row in df_tools[:1]:
    tools_list.append(row)


# input buttons data
rows_btns = df.iterrows()

# output buttons data
columns_btns = []
for column in df.iteritems():
    columns_btns.append(column[0])

app = Flask(__name__)
app.secret_key = "asd"

# TODO check what happens if more than 5 tools are being brought up in the results
# TODO add an all tools tab in the navbar, for the user to see what exists and what doesn't
# TODO check if the website works on the tresorit,
#  maybe convert to desktop application (flask-desktop), maybe store on python anywhere

inputs_list = []
rows_btns = df.iterrows()
for row in rows_btns:
    inputs_list.append(row[0])

outputs_list = []
for column in df.iteritems():
    outputs_list.append(column[0])


# homepage
@app.route('/', methods=["POST", "GET"])
def hello(name=None):

    # data table format
    df = pd.read_csv("data1.csv")
    columns_strip_dict = {}
    df.set_index("inputs", inplace=True)
    for column in df:
        columns_strip_dict[column] = lambda x: x.strip("[]").split(", ")
    df = pd.read_csv("data1.csv", converters=columns_strip_dict)
    df.set_index("inputs", inplace=True)

    # tools table format
    df_tools = pd.read_csv("tools1.csv")
    df_tools.set_index("name", inplace=True)
    only_tools_dict = df_tools.to_dict()

    tools_list = []
    for row in df_tools[:1]:
        tools_list.append(row)

    # input buttons data
    rows_btns = df.iterrows()

    # output buttons data
    columns_btns = []
    for column in df.iteritems():
        columns_btns.append(column[0])

    if request.method == "POST":
        input_ans = request.form.getlist("input")
        input_ans_1 = input_ans[0]
        print(input_ans_1)
        output_ans = request.form.getlist("output")
        output_ans_1 = output_ans[0]
        print(output_ans_1)
        session["tools"] = df[input_ans_1][output_ans_1]
        session["input_ans"] = input_ans_1
        session["output_ans"] = output_ans_1
        return redirect(url_for("answer"))
    else:
        return render_template("index.html", name=name, df=df, inputs=inputs_list, outputs=outputs_list)


# result page
@app.route('/result', methods=["POST", "GET"])
def answer():
    # data table format
    df = pd.read_csv("data1.csv")
    columns_strip_dict = {}
    df.set_index("inputs", inplace=True)
    for column in df:
        columns_strip_dict[column] = lambda x: x.strip("[]").split(", ")
    df = pd.read_csv("data1.csv", converters=columns_strip_dict)
    df.set_index("inputs", inplace=True)

    # tools table format
    df_tools = pd.read_csv("tools1.csv")
    df_tools.set_index("name", inplace=True)
    only_tools_dict = df_tools.to_dict()

    tools_list = []
    for row in df_tools[:1]:
        tools_list.append(row)

    # input buttons data
    rows_btns = df.iterrows()

    # output buttons data
    columns_btns = []
    for column in df.iteritems():
        columns_btns.append(column[0])

    tools_dict = {}
    tools = session.pop("tools", None)
    print(f'tools are {tools}')
    input_ans = session.pop("input_ans", None)
    output_ans = session.pop("output_ans", None)
    print(f'{input_ans} and {output_ans}')
    for tool in tools:
        print(tool)
        if tool in tools_list:
            tools_dict[tool] = {"photo": df_tools[tool]["photo"], "link":  df_tools[tool]["link"], "date":df_tools[tool]["date"]}
    dict_len = len(tools_dict)

    # TODO i need to make the dictionary divided by every two keys, so i can put them in a bootstrap row later, or find another way to present as every two

    return render_template('result.html', tools=tools, tools_dict=tools_dict, df=df, inputs=inputs_list, outputs=outputs_list, input_ans=input_ans, output_ans= output_ans, dict_len=dict_len)


# Add tool page
@app.route('/addtool', methods=["POST", "GET"])
def adder(name=None):

    # data table format
    df = pd.read_csv("data1.csv")
    columns_strip_dict = {}
    df.set_index("inputs", inplace=True)
    for column in df:
        columns_strip_dict[column] = lambda x: x.strip("[]").split(", ")
    df = pd.read_csv("data1.csv", converters=columns_strip_dict)
    df.set_index("inputs", inplace=True)

    # tools table format
    df_tools = pd.read_csv("tools1.csv")
    df_tools.set_index("name", inplace=True)
    only_tools_dict = df_tools.to_dict()

    tools_list = []
    for row in df_tools[:1]:
        tools_list.append(row)

    if request.method == "POST":
        # text inputs var set
        photo_link = request.form.get("photolink")
        current_date = request.form.get("currentdate")
        tool_link = request.form.get("toollink")
        tool_name = request.form.get("toolname")

        # check good input and then add new tool to the database(csv)
        if photo_link and current_date and tool_name is not None:
            index_to_rid = [photo_link, tool_link, current_date]
            df_tools_1 = df_tools.assign(index_to_rid=index_to_rid)
            df_tools_1.rename(columns={"index_to_rid": tool_name}, inplace=True)
            df_tools_1.to_csv("tools1.csv")

        # input output assignments
        assignments_dict = {}
        for num in range(1,9):
            if tool_name and request.form.get(f"input_check_{num}") and request.form.get(f"output_check_{num}") is not None:
                recieved_input = request.form.get(f"input_check_{num}")
                recieved_output = request.form.get(f"output_check_{num}")
                assignments_dict[num] = [recieved_input, recieved_output]
        for assignment in assignments_dict:
            input_check = assignments_dict[assignment][0]  # full name
            output_check = assignments_dict[assignment][1]  # phone
            list_existing_tools = df[input_check][output_check]
            list_existing_tools.append(tool_name)
            print(list_existing_tools)
            list_to_str = ", ".join(list_existing_tools)
            list_final = "[" + list_to_str + "]"
            print(list_final)

            df_new = pd.read_csv("data1.csv")
            df_new.set_index("inputs", inplace=True)
            df_new[input_check][output_check] = list_final
            print(df_new)
            df_new.to_csv("data1.csv")
        # TODO write the dictionary to data1
        return redirect(url_for("adder"))
    return render_template('adder.html', name=name, df=df, inputs=inputs_list, outputs=outputs_list)


# All tools page
@app.route('/alltools', methods=["POST", "GET"])
def all_tools_view(name=None):

    # tools table format
    df_tools = pd.read_csv("tools1.csv")
    df_tools.set_index("name", inplace=True)
    only_tools_dict = df_tools.to_dict()

    tools_list = []
    for row in df_tools[:1]:
        tools_list.append(row)

    x = 5
    list_of_lists = [tools_list[i:i+x] for i in range(0, len(tools_list), x)]
    print(list_of_lists)
    return render_template('alltools.html', only_tools_dict=only_tools_dict, tools_list=tools_list, list_of_lists=list_of_lists)


if __name__ == "__main__":
    app.run(debug=True)








