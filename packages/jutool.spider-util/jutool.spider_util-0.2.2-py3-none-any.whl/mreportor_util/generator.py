import time, importlib, inspect, os
from code_util.markdown import draw_markdownobj_flowchart, markdowndoc, flowchart_color_enum, flowchart_shape_enum, \
    draw_markdownobj_gantt
from code_util.structures import iter_idx
from code_util.log import log_error
from mreportor_util.structions import *


class _act_node:
    def __init__(self, type_s: node_base, file_path: str, class_name: str):
        self.ID_Name = type_s.__name__
        self.Type_S = type_s
        self.Name = type_s.Name()
        self.File_Path = file_path
        self.Class_Name = class_name


class _mind_node:
    def __init__(self, type_s: node_base):
        self.ID_Name = type_s.__name__
        self.Type_S = type_s

        self.Name = type_s.Name()
        self.ALL_Act_Nodes = {}

    def date_info(self) -> {str: {str: (str, str)}}:
        r_dict = {}
        for act_key, act in self.ALL_Act_Nodes.items():
            sub_dict = {}
            work_sp = act.Type_S.work_timespan()
            opt_sp = act.Type_S.optimize_timespans()

            if work_sp is not None:
                sub_dict['working'] = work_sp

            if opt_sp is not None:
                for k, v in opt_sp.items():
                    sub_dict[k] = v

            if len(sub_dict) > 0:
                r_dict[act.Name] = sub_dict

        if len(r_dict) == 0:
            return None
        return r_dict


class _goal_node:
    def __init__(self, type_s: node_base):
        self.ID_Name = type_s.__name__
        self.Type_S = type_s
        self.Name = type_s.Name()

        self.ALL_Minds_Nodes = {}
        self.ALL_Paths = []

    def prepare(self):
        self._get_all_path_of_goals()

    def _get_all_path_of_goals(self):

        if len(self.ALL_Minds_Nodes.keys()) == 0:
            return

        item_map = {}
        header_map = {}

        def recu_item(key, stop_name, node: [], lines: []):
            if key == stop_name:
                return
            if key in header_map:
                for item in header_map[key]:
                    node.append(item)
                    lines.append((key, item))
                    recu_item(item, stop_name, node, lines)

        for s_key, node in self.ALL_Minds_Nodes.items():
            item_map[s_key] = node.Type_S
            s_node = node.Type_S
            f_node = s_node.from_node()
            if f_node is not None:
                if f_node.__name__ not in header_map:
                    header_map[f_node.__name__] = set()
                header_map[f_node.__name__].add(s_node.__name__)
            t_node = s_node.target_node()
            if t_node is not None:
                if s_node.__name__ not in header_map:
                    header_map[s_node.__name__] = set()
                header_map[s_node.__name__].add(t_node.__name__)

        for start_key in header_map[self.ID_Name]:
            cur_node = []
            cur_line = []
            recu_item(start_key, self.ID_Name, cur_node, cur_line)
            cur_node.append(start_key)
            cur_line.append((self.ID_Name, start_key))
            self.ALL_Paths.append((cur_node, cur_line))


def _line_name(from_item, target_item):
    return f"{from_item.__name__}_{target_item.__name__}"


def _draw_goal_mark_graph(nodes_dict, doc_obj):
    line_dict = {}
    for cls_key in nodes_dict.keys():
        cls = cls_key, nodes_dict[cls_key].Type_S
        from_node = cls[1].from_node()
        if from_node is not None:
            key = _line_name(from_node, cls[1])
            if key not in line_dict:
                line_dict[key] = []
                line_dict[key].append({
                    'from': from_node,
                    'to': cls[1],
                    'message': cls[1].from_node_message(),
                    'version': cls[1].Version(),
                    'main_body': cls[1]
                })
        target_node = cls[1].target_node()
        if target_node is not None:
            key = _line_name(cls[1], target_node)
            if key not in line_dict:
                line_dict[key] = []
                line_dict[key].append({
                    'from': cls[1],
                    'to': target_node,
                    'message': cls[1].target_message(),
                    'version': cls[1].Version(),
                    'main_body': cls[1]
                })

    doc_obj.write_title("需求梳理框架", 1)

    chart1 = draw_markdownobj_flowchart()
    for key in nodes_dict.keys():
        item = nodes_dict[key].Type_S
        chart1.add_node(item.Name(), item.__name__)
    for line in line_dict.keys():
        sorted(line_dict[line], key=lambda s: s['version'])
        last_version = line_dict[line][-1]

        if last_version['from'].state() == node_state_enum.Abandon:
            chart1.add_line(last_version['from'].__name__, last_version['to'].__name__, last_version['message'],
                            dot_line=True)
        else:
            chart1.add_line(last_version['from'].__name__, last_version['to'].__name__, last_version['message'])

    doc_obj.write_markdownobj(chart1)


def _remove_left_strip(str_list):
    for _ in range(100):
        for s in str_list:
            if s == "":
                continue
            if s[0] != " ":
                return str_list

        str_list = [x[1:] for x in str_list if x != ""]

    return None


def _find_all_modules(folder: []):
    result_dict = []
    result_time_dict = []
    for module_ in folder:
        for path, dir_name, file_names in os.walk(module_):
            path_pre = ".".join([x for x in os.path.split(path) if x])

            if path.startswith('_'):
                continue

            for filename in file_names:
                if filename.startswith('_') or "__pycache__" in filename or "__pycache__" in path_pre:
                    continue

                file_full_path = os.path.join(path, filename)
                module_edit_time = os.stat(file_full_path).st_mtime
                module_create_time = os.stat(file_full_path).st_ctime

                module_name = path_pre + "." + filename.replace('.py', '')
                result_dict.append(module_name)
                result_time_dict.append((module_create_time, module_edit_time, os.path.join(path, filename)))
    return zip(result_dict, result_time_dict)


def _draw_report(goal_nodes_nodes, doc: markdowndoc):
    _draw_goal_mark_graph(goal_nodes_nodes, doc)

    for goal_key, goal in goal_nodes_nodes.items():
        if len(goal.ALL_Paths) == 0:
            continue

        doc.write_title(goal.Name, 1)
        # mind_path
        for (path_nodes, path_lines), idex in iter_idx(goal.ALL_Paths):
            mind_group_name = f"{goal.Name}-研究思路({idex + 1})"
            doc.write_title(mind_group_name, 2)

            # _draw_mind_graph(doc, goal_mark_nodes_dict, mind_step_obj_node_dict, act_step_node_dict, cls_key,
            #                  arrange_info[0], arrange_info[1], mind_group_name)

            # mind_chart

            doc.write_title("方案介绍", 3)
            chart1 = draw_markdownobj_flowchart()
            ordered_path_nodes = sorted(path_nodes, key=lambda x: 1 if x == goal.ID_Name else 2)
            for n in ordered_path_nodes:
                if n == goal.ID_Name:
                    chart1.add_node("@@" + goal.Name, n, icon="fa-rocket")
                    chart1.set_node_color(n, color=flowchart_color_enum.NavajoWhite)
                    chart1.set_node_shape(n, shape=flowchart_shape_enum.Circle)
                else:
                    chart1.add_node("@@" + goal.ALL_Minds_Nodes[n].Name, n,
                                    anchor_title="@@" + goal.ALL_Minds_Nodes[n].Name,
                                    icon="fa-cog")
                    chart1.set_node_shape(n, shape=flowchart_shape_enum.Hexagon)

            for l in path_lines:
                chart1.add_line(l[0], l[1])
            doc.write_markdownobj(chart1)

            # mind的思路讲解
            for node_arr in path_nodes:
                if node_arr in goal.ALL_Minds_Nodes:
                    node_doc = goal.ALL_Minds_Nodes[node_arr].Type_S.__doc__
                    if node_doc is not None:
                        doc.write_line("- " + node_doc.strip())

            doc.write_title("结论概述", 3)
            # 结论
            tabledatas2 = []
            for node_arr in path_nodes:
                if node_arr in goal.ALL_Minds_Nodes:
                    node = goal.ALL_Minds_Nodes[node_arr].Type_S
                    name = goal.ALL_Minds_Nodes[node_arr].Name
                    act_count = len(goal.ALL_Minds_Nodes[node_arr].ALL_Act_Nodes)
                    state_method = node.state
                    state = state_method()
                    docs = state_method.__doc__
                    doca = docs if docs is not None else ""
                    if act_count != 0:
                        tabledatas2.append([f"[@{name}](#@@{name})", name, str(act_count), str(state.name), doca])
                    else:
                        tabledatas2.append([f" ", name, str(act_count), str(state.name), doca])

            doc.write_table(["序号", "模块名称", "调研方法个数", "状态", "结论"], tabledatas2)

            ## gantt
            doc.write_title("时间进度", 3)
            gatte_chart = draw_markdownobj_gantt("时间表")
            for node_arr in path_nodes:
                if node_arr in goal.ALL_Minds_Nodes:
                    date_info = goal.ALL_Minds_Nodes[node_arr].date_info()
                    if date_info is not None:
                        # doc.write_markdown_code("\n\n**工作时间表**\n")
                        for gant_item, g_dates in date_info.items():
                            gatte_chart.add_item("@" + gant_item)
                            for g_one_key, g_one_data in g_dates.items():
                                gatte_chart.add_item_data("@" + gant_item, gant_item, g_one_data)
            doc.write_markdownobj(gatte_chart)

            doc.write_title("模块详细信息", 3)
            # per_mind chart
            for n in path_nodes:
                if n == goal.ID_Name:
                    continue

                if len(goal.ALL_Minds_Nodes[n].ALL_Act_Nodes) == 0:
                    doc.write_title(goal.ALL_Minds_Nodes[n].Name, 4)
                    continue

                doc.write_title(goal.ALL_Minds_Nodes[n].Name, 4)

                mind_chart1 = draw_markdownobj_flowchart()

                mind_chart1.add_node("@@" + goal.ALL_Minds_Nodes[n].Name, n,
                                     anchor_title="@@" + goal.ALL_Minds_Nodes[n].Name,
                                     icon="fa-cog")
                mind_chart1.set_node_shape(n, shape=flowchart_shape_enum.Hexagon)

                for key, val in goal.ALL_Minds_Nodes[n].ALL_Act_Nodes.items():
                    act_state = val.Type_S.state()

                    if act_state == node_state_enum.Notset:
                        mind_chart1.add_node("@@" + val.Name, key, anchor_title="@@" + val.Name, icon="fa-question")
                        mind_chart1.set_node_color(key, flowchart_color_enum.Orange)

                    if act_state == node_state_enum.Abandon:
                        mind_chart1.add_node("@@" + val.Name, key, anchor_title="@@" + val.Name, icon="fa-close")
                        mind_chart1.set_node_color(key, flowchart_color_enum.Orange)

                    if act_state == node_state_enum.InOptimize:
                        mind_chart1.add_node("@@" + val.Name, key, anchor_title="@@" + val.Name, icon="fa-magic")
                        mind_chart1.set_node_color(key, flowchart_color_enum.DeepSkyBlue)

                    if act_state == node_state_enum.Completed:
                        mind_chart1.add_node("@@" + val.Name, key, anchor_title="@@" + val.Name, icon="fa-check")
                        mind_chart1.set_node_color(key, flowchart_color_enum.Auqamarin)

                    if act_state == node_state_enum.InWork:
                        mind_chart1.add_node("@@" + val.Name, key, anchor_title="@@" + val.Name, icon="fa-spinner")
                        mind_chart1.set_node_color(key, flowchart_color_enum.DeepSkyBlue)

                    mind_chart1.set_node_shape(key, flowchart_shape_enum.Stadium)
                    mind_chart1.add_line(key, n)

                doc.write_markdownobj(mind_chart1)

                # 结论
                tabledatas = []
                for key, act in goal.ALL_Minds_Nodes[n].ALL_Act_Nodes.items():
                    name = act.Name
                    state_method = act.Type_S.state
                    state = state_method()
                    docs = state_method.__doc__
                    tabledatas.append([name, state, docs])

                # tabledatas.sort(key=lambda x: x[2], reverse=True)
                n_table_datas = []
                for nn, state, doca in tabledatas:
                    # ftime = f"{time.strftime('%Y-%m-%d', time.localtime(s))}~{time.strftime('%Y-%m-%d', time.localtime(e))}"
                    doca = doca if doca is not None else ""
                    # n_table_datas.append([f"[{nn}](#{nn.lower().replace(' ', '-')})", str(state.name), doca])
                    n_table_datas.append([f"[@{nn}](#@@{nn})", nn, str(state.name), doca])

                doc.write_table(["序号", "act名称", "状态", "结论"], n_table_datas)

                # ## gantt
                # date_info = goal.ALL_Minds_Nodes[n].date_info()
                # if date_info is not None:
                #     # doc.write_markdown_code("\n\n**工作时间表**\n")
                #     gatte_chart = draw_markdownobj_gantt("时间表")
                #     for gant_item, g_dates in date_info.items():
                #         gatte_chart.add_item("@" + gant_item)
                #         for g_one_key, g_one_data in g_dates.items():
                #             gatte_chart.add_item_data("@" + gant_item, g_one_key, g_one_data)
                #     doc.write_markdownobj(gatte_chart)

                ## act 详解
                # doc.write_title(mind_dic[n].Name(), 4)
                for key, act in goal.ALL_Minds_Nodes[n].ALL_Act_Nodes.items():
                    act_doc = act.Type_S.__doc__
                    if act_doc is not None:
                        doc.write_title(act.Name, 5)
                        doc.write_markdown_code(f"*file location* : **{act.File_Path}** \n")
                        doc.write_markdown_code(f"*class name* : **{act.Class_Name}** \n")
                        splited_strlist = act_doc.split('\n')
                        splited_strlist = _remove_left_strip(splited_strlist)
                        for doc_line_str in splited_strlist:
                            if doc_line_str.endswith("//"):
                                doc.write_markdown_code(doc_line_str)
                            else:
                                doc.write_markdown_code(doc_line_str + '\n')

                    key_method_list = act.Type_S.key_methods()
                    if len(key_method_list) > 0:
                        doc.write_line("关键代码", True)
                        for key_f in key_method_list:
                            source = inspect.getsource(key_f)
                            doc.write_code(source)
                    act.Type_S.custom_out(doc)

                    # doc.write_markdown_code(f"[返回](#{navi_back_title.lower().replace(' ', '-')})\n")

                    doc.write_markdown_code(f"[返回方案](#@@{goal.Name}-研究思路({idex + 1}))\n")


def generator_report(solution_name: str, module_list: [], path):
    doc = markdowndoc(path, True, title_with_index=True)

    all_goal_dict = {}
    all_goal_dict[goal_mark_start.__name__] = _goal_node(goal_mark_start)

    all_mind_dict = {}
    all_act_dict = {}

    for module_, times_ in _find_all_modules(module_list):
        module_obj = importlib.import_module(module_)
        all_classes = inspect.getmembers(module_obj, inspect.isclass)
        for cls in all_classes:
            if not issubclass(cls[1], node_base) or cls[1].__module__ != module_:
                continue
            if issubclass(cls[1], goal_mark) and cls[0] not in all_goal_dict:
                all_goal_dict[cls[1].__name__] = _goal_node(cls[1])

            if issubclass(cls[1], mind_step):
                # all_mind_dict[cls[1].__name__] = cls[1]
                goal_type = cls[1].base_node()
                if goal_type.__name__ not in all_mind_dict:
                    all_mind_dict[goal_type.__name__] = []
                all_mind_dict[goal_type.__name__].append(_mind_node(cls[1]))

            if issubclass(cls[1], act_step):
                base_node = cls[1].base_node()
                if base_node.__name__ not in all_act_dict:
                    all_act_dict[base_node.__name__] = []

                file_path = os.path.join(*module_.split('.'))
                all_act_dict[base_node.__name__].append(_act_node(cls[1], file_path, cls[0]))

    # merge all_mind_dict and all_act_dict
    index_mind_2_goal = {}
    for key, value in all_mind_dict.items():
        for item in value:
            all_goal_dict[key].ALL_Minds_Nodes[item.ID_Name] = item
            index_mind_2_goal[item.ID_Name] = key
    for key, value in all_act_dict.items():
        for item in value:
            gold_key = index_mind_2_goal[key]
            all_goal_dict[gold_key].ALL_Minds_Nodes[key].ALL_Act_Nodes[item.ID_Name] = item

    for _goal_node_item in all_goal_dict.values():
        _goal_node_item.prepare()

    _draw_report(all_goal_dict, doc)

    doc.write_footer()
    doc.flush()

    time.time()

    # _recu_node(end_node)
