"""Main file for testing the program."""

import shutil
from pathlib import Path

from controllers.configuration import (
    get_user_configs,
    set_model_configs,
    update_config_file,
)
from controllers.data_visualizations import create_save_graph
from controllers.processes import (
    create_wordclouds,
    load_conversations_from_zip,
    write_custom_instructions,
    write_markdown_files,
)


def main() -> None:
    """Main function."""

    print(
        "Welcome to ChatGPT Data Visualizer ✨📊!\n\n"
        "Follow the instructions in the command line.\n\n"
        "Press 'ENTER' to select the default options.\n\n"
        "If you encounter any issues, please report them here:\n\n"
        "🐛 🚨 https://github.com/mohamed-chs/chatgpt-history-export-to-md/issues/new/choose 🔗\n\n"
    )

    # -------------- getting configs --------------

    configs = get_user_configs()
    set_model_configs(configs)

    print("\n\nAnd we're off! 🚀🚀🚀\n")

    # -------------- loading data --------------

    print("Loading data 📂 ...\n")

    zip_filepath = Path(configs["zip_filepath"])

    all_conversations_list = load_conversations_from_zip(zip_filepath)

    # -------------- creating output folder --------------

    output_folder = Path(configs["output_folder"])

    if output_folder.exists() and output_folder.is_dir():
        shutil.rmtree(output_folder)

    output_folder.mkdir(parents=True, exist_ok=True)

    # --------- writing markdown files ---------

    markdown_folder = output_folder / "Markdown"
    markdown_folder.mkdir(parents=True, exist_ok=True)

    write_markdown_files(all_conversations_list, markdown_folder)

    print(f"\nDone 🎉 ! Check the output 📄 here : {markdown_folder.as_uri()} 🔗\n")

    # ----------- creating graphs -------------

    graph_folder = output_folder / "Graphs"
    graph_folder.mkdir(parents=True, exist_ok=True)

    # for week in tqdm(weeks_dict.keys(), desc="Creating weekly graphs 📈 ..."):
    #     all_week_timestamps = [
    #         node.message.create_time
    #         for convo in weeks_dict[week]
    #         for node in convo.user_nodes + convo.assistant_nodes
    #         if node.message and node.message.create_time
    #     ]

    #     create_save_graph(
    #         all_week_timestamps, graph_folder / f"{week.strftime('week %d %m %Y')}.png"
    #     )

    # for month in tqdm(months_dict.keys(), desc="Creating monthly graphs 📈 ..."):
    #     all_month_timestamps = [
    #         node.message.create_time
    #         for convo in months_dict[month]
    #         for node in convo.user_nodes + convo.assistant_nodes
    #         if node.message and node.message.create_time
    #     ]

    #     create_save_graph(
    #         all_month_timestamps, graph_folder / f"{month.strftime('%B')}.png"
    #     )

    print("Creating graph 📈 of prompts per day ...\n")

    graph_path = graph_folder / "all messages.png"

    create_save_graph(all_conversations_list.all_message_timestamps(), graph_path)

    print(f"\nDone 🎉 ! Check the output 📈 here : {graph_folder.as_uri()} 🔗\n")
    print("(more graphs 📈 will be added in the future ...)\n")

    # ----------- creating bar charts -------------

    # print("Creating bar charts 📊 ...\n")

    # bar_chart_folder = output_folder / "Bar Charts"
    # bar_chart_folder.mkdir(parents=True, exist_ok=True)

    # # bar chart logic here ...

    # print(f"\nDone 🎉 ! Check the output 📊 here : {bar_chart_folder.as_uri()} 🔗\n")

    # ----------- creating wordclouds -------------

    wordcloud_folder = output_folder / "Word Clouds"
    wordcloud_folder.mkdir(parents=True, exist_ok=True)

    create_wordclouds(all_conversations_list, wordcloud_folder, configs)

    print(f"\nDone 🎉 ! Check the output 🔡☁️ here : {wordcloud_folder.as_uri()} 🔗\n")

    # ----------- creating heatmaps -------------

    # print("Creating heatmaps 🗺️ ...\n")

    # heatmap_folder = output_folder / "Heatmaps"
    # heatmap_folder.mkdir(parents=True, exist_ok=True)

    # # heatmap logic here ...

    # print(f"\nDone 🎉 ! Check the output 🗺️ here : {heatmap_folder.as_uri()} 🔗\n")

    # ------------- writing custom instructions --------------

    print("Writing custom instructions 📝 ...\n")

    ci_json_filepath = output_folder / "custom_instructions.json"

    write_custom_instructions(all_conversations_list, ci_json_filepath)

    print(f"\nDone 🎉 ! Check the output 📝 here : {ci_json_filepath.as_uri()} 🔗\n")

    # ------------ Done ! saving configs ... -------------

    update_config_file(configs)

    print("(Settings ⚙️ have been updated and saved to 'config.json')\n")

    print(
        "ALL DONE 🎉🎉🎉 !\n\n"
        f"Explore the full gallery 🖼️ at: {output_folder.as_uri()} 🔗\n\n"
        "I hope you enjoy the outcome 🤞.\n\n"
        "If you appreciate it, kindly give the project a star 🌟 on GitHub :\n\n"
        "➡️ https://github.com/mohamed-chs/chatgpt-history-export-to-md 🔗\n\n"
    )


if __name__ == "__main__":
    main()
