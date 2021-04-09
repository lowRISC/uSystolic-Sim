import os
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib
from numpy import mean, median

def plot_fig(technode=""):
    font = {'family':'Times New Roman', 'size': 6}
    matplotlib.rc('font', **font)

    print_power_onchip = True
    print_power_total = True
    print_energy_onchip = True
    print_energy_total = True
    print_area = True

    bw_sram_dram = True

    if not os.path.exists("./outputs_fig/"):
        os.system("mkdir ./outputs_fig")

    arch_list = ["tpu", "eyeriss"]
    network_list = ["alexnet"]
    bit_list = ["8", "16"]
    cycle_list = ["32", "64", "128"]
    ram_list = ["ddr3_w__spm", "ddr3_wo_spm"]

    for a in arch_list:
        bw_list = []
        time_list = []
        tp_list = []
        area_list = []
        power_list = []
        energy_list = []
        if a == "tpu":
            a_cap = "TPU"
        else:
            a_cap = "Eyeriss"

        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ")
        print("Processing " + a + ":")
        print("# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # ")
        
        for b in bit_list:
            for n in network_list:
                for r in ram_list:
                    # binary parallel
                    computing = "bp"
                    name = a + "_" + b.zfill(2) + "b_" + computing + "_" + "001c_" + n + "_" + r
                    if not os.path.exists("./outputs/" + technode + "/" + name):
                        raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                    
                    path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                    time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                    tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                    
                    path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L
                    
                    # binary serial
                    computing = "bs"
                    name = a + "_" + b.zfill(2) + "b_" + computing + "_" + b.zfill(3) + "c_" + n + "_" + r
                    if not os.path.exists("./outputs/" + technode + "/" + name):
                        raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                    
                    path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                    bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                    time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                    tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                    
                    path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                    area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                    power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                    energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L

                    # unary rate
                    computing = "ur"
                    for c in cycle_list:
                        name = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        if not os.path.exists("./outputs/" + technode + "/" + name):
                            raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                        
                        path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                        time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                        tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                        
                        path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L

                    # unary temporal
                    computing = "ut"
                    for c in cycle_list:
                        name = a + "_" + b.zfill(2) + "b_" + computing + "_" + c.zfill(3) + "c_" + n + "_" + r
                        if not os.path.exists("./outputs/" + technode + "/" + name):
                            raise ValueError("Folder ./outputs/" + technode + "/" + name + " does not exist.")
                        
                        path = "./outputs/" + technode + "/" + name + "/simHwOut/"
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=6)) # dram bw
                        bw_list.append(return_indexed_elems(    input_csv=path + name + "_avg_bw_real.csv",     index=11)) # sram bw
                        time_list.append(return_indexed_elems(  input_csv=path + name + "_throughput_real.csv", index=3)) # runtime
                        tp_list.append(return_indexed_elems(    input_csv=path + name + "_throughput_real.csv", index=4)) # throughput
                        
                        path = "./outputs/" + technode + "/" + name + "/simEffOut/"
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=8)) # sram area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=9)) # sa ireg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=10)) # sa wreg area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=11)) # sa mul area
                        area_list.append(return_indexed_elems(  input_csv=path + name + "_area.csv",            index=12)) # sa acc area
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=6)) # dram
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=11)) # sram D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=15)) # sram L
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=29)) # sa D
                        power_list.append(return_indexed_elems( input_csv=path + name + "_power.csv",           index=30)) # sa L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=6)) # dram
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=11)) # sram D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=15)) # sram L
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=29)) # sa D
                        energy_list.append(return_indexed_elems(input_csv=path + name + "_energy.csv",          index=30)) # sa L

        if bw_sram_dram:
            # bandwidth
            my_dpi = 300
            if a == "eyeriss":
                fig_h = 2
            else:
                fig_h = 1.5
            fig_w = 3.3115

            bp_color = "#7A81FF"
            bs_color = "#FF7F7F"
            u6_color = "#666666"
            u7_color = "#888888"
            u8_color = "#AAAAAA"
            bg_color = "#D783FF"

            x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

            fig, ax = plt.subplots(figsize=(fig_w, fig_h))
            
            idx_tot = 10

            x_idx = np.arange(len(x_axis))

            width = 1 / 2**(math.ceil(math.log2(idx_tot)))

            iterval = width
            
            # 8b - spm - bp
            index = 0
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx = 0.5
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=bp_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - spm - bs
            index = 1
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=bs_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - spm - ur - 32c
            index = 2
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u6_color, label="Unary-32c")
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u6_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - spm - ur - 64c
            index = 3
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u7_color, label="Unary-64c")
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u7_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - spm - ur - 128c
            index = 4
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u8_color, label="Unary-128c")
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u8_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - wospm - bp
            index = 8
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bp_color)
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=bp_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - wospm - bs
            index = 9
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bs_color)
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=bs_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - wospm - ur - 32c
            index = 10
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u6_color)
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u6_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - wospm - ur - 64c
            index = 11
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u7_color)
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u7_color)
            # print(dram_bw_list, sram_bw_list)

            # 8b - wospm - ur - 128c
            index = 12
            dram_bw_list = bw_list[index * 2][:-1]
            sram_bw_list = [-x for x in bw_list[index * 2 + 1][:-1]]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u8_color)
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_bw_list, width, hatch = None, alpha=0.99, color=u8_color)
            # print(dram_bw_list, sram_bw_list)

            ax.set_ylabel('SRAM-DRAM bandwidth (GB/s)')
            ax.set_xticks(x_idx)
            ax.set_xticklabels(x_axis)
            plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
            bottom, top = plt.ylim()

            if a == "eyeriss":
                ax.set_ylim((bottom, top*350))
                bottom, top = plt.ylim()
                for x in x_idx:
                    ax.fill_betweenx([bottom, top/350], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
                ax.legend(loc="upper center", ncol=3, frameon=True)
            else:
                ax.set_ylim((bottom, top))
                bottom, top = plt.ylim()
                for x in x_idx:
                    ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.axhline(y=0, color="k", linewidth = 0.1)
            
            plt.yscale("symlog", linthreshy=0.001)
            locs, labels = plt.yticks()
            if a == "eyeriss":
                locs = locs[:-2]
            else:
                locs = locs
            ax.set_yticks(locs)
            y_label_list = []
            for y in locs:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
            fig.tight_layout()
            plt.savefig('./outputs_fig/' + technode + '/Bandwidth_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
            print("Bandwidth fig saved!\n")
        else:
            # bandwith
            my_dpi = 300
            if a == "eyeriss":
                fig_h = 1.5
            else:
                fig_h = 1
            fig_w = 3.3115

            bp_color = "#7A81FF"
            bs_color = "#FF7F7F"
            u6_color = "#666666"
            u7_color = "#888888"
            u8_color = "#AAAAAA"
            bg_color = "#D783FF"

            x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

            fig, ax = plt.subplots(figsize=(fig_w, fig_h))
            
            idx_tot = 10

            x_idx = np.arange(len(x_axis))

            width = 1 / 2**(math.ceil(math.log2(idx_tot)))

            iterval = width

            # 8b - spm - bp
            index = 0
            dram_bw_list = bw_list[index * 2][:-1]
            idx = 0.5
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")

            # 8b - spm - bs
            index = 1
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")

            # 8b - spm - ur - 32c
            index = 2
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u6_color, label="Unary-32c")

            # 8b - spm - ur - 64c
            index = 3
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u7_color, label="Unary-64c")

            # 8b - spm - ur - 128c
            index = 4
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u8_color, label="Unary-128c")

            # 8b - wospm - bp
            index = 8
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bp_color)

            # 8b - wospm - bs
            index = 9
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=bs_color)

            # 8b - wospm - ur - 32c
            index = 10
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u6_color)

            # 8b - wospm - ur - 64c
            index = 11
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u7_color)

            # 8b - wospm - ur - 128c
            index = 12
            dram_bw_list = bw_list[index * 2][:-1]
            idx += 1
            ax.bar(x_idx + iterval * (idx - idx_tot / 2), dram_bw_list, width, hatch = None, alpha=0.99, color=u8_color)

            ax.set_ylabel('Bandwith (GB/s)')
            ax.set_xticks(x_idx)
            ax.set_xticklabels(x_axis)
            plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
            plt.yscale("log")

            _, top = plt.ylim()

            locs, labels = plt.yticks()
            if a == "eyeriss":
                locs = [0.001, 0.01, 0.1, 1, 10]
            else:
                locs = [0.001, 0.01, 0.1, 1, 10]
            ax.set_yticks(locs)
            
            bottom, _ = plt.ylim()
            if a == "eyeriss":
                ax.set_ylim((bottom, top*40))
                bottom, top = plt.ylim()
                for x in x_idx:
                    ax.fill_betweenx([bottom, top/40], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
                ax.legend(loc="upper center", ncol=3, frameon=True)
            else:
                ax.set_ylim((bottom, top))
                bottom, top = plt.ylim()
                for x in x_idx:
                    ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            
            y_label_list = []
            for y in locs:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)

            ax.minorticks_off()
            fig.tight_layout()
            plt.savefig('./outputs_fig/' + technode + '/Bandwidth_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
            print("Bandwidth fig saved!\n")


        # runtime
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.5
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        bg_color = "#D783FF"

        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 5

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width

        # 8b - spm - bp
        index = 0
        runtime_list = time_list[index][:-1]
        idx = 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")

        # 8b - spm - bs
        index = 1
        runtime_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")

        # 8b - wospm - ur - 32c
        index = 10
        runtime_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=u6_color, label="Unary-32c")

        # 8b - wospm - ur - 64c
        index = 11
        runtime_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=u7_color, label="Unary-64c")

        # 8b - wospm - ur - 128c
        index = 12
        runtime_list = time_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), runtime_list, width, hatch = None, alpha=0.99, color=u8_color, label="Unary-128c")

        ax.set_ylabel('Runtime (Seconds)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("log")

        _, top = plt.ylim()

        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[1:-1]
        else:
            locs = locs[1:]
        ax.set_yticks(locs)
        
        bottom, _ = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((bottom, top*8))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/8], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Runtime_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Runtime fig saved!\n")


        # throughput
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.5
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        bg_color = "#D783FF"

        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 5

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width

        # 8b - spm - bp
        index = 0
        throughput_list = tp_list[index][:-1]
        idx = 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list, width, hatch = None, alpha=0.99, color=bp_color, label="Binary Parallel")

        # 8b - spm - bs
        index = 1
        throughput_list = tp_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list, width, hatch = None, alpha=0.99, color=bs_color, label="Binary Serial")

        # 8b - wospm - ur - 32c
        index = 10
        throughput_list = tp_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list, width, hatch = None, alpha=0.99, color=u6_color, label="Unary-32c")

        # 8b - wospm - ur - 64c
        index = 11
        throughput_list = tp_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list, width, hatch = None, alpha=0.99, color=u7_color, label="Unary-64c")

        # 8b - wospm - ur - 128c
        index = 12
        throughput_list = tp_list[index][:-1]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), throughput_list, width, hatch = None, alpha=0.99, color=u8_color, label="Unary-128c")

        ax.set_ylabel('Throughput (Frames/s)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("log")

        _, top = plt.ylim()

        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[1:-1]
        else:
            locs = locs[1:]
        ax.set_yticks(locs)
        
        bottom, _ = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((bottom, top*10))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/10], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Throughput_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Throughput fig saved!\n")


        # area
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1.5
        else:
            fig_h = 1.5
        fig_w = 3.3115

        x_axis = ["SRAM-8b", "BP-8b", "BS-8b", "UR-8b", "UT-8b", "SRAM-16b", "BP-16b", "BS-16b", "UR-16b", "UT-16b"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        x_idx = np.arange(len(x_axis))

        width = 0.4

        index = 0
        sram_list = [
                        area_list[ 0 * 5 + index][0], area_list[ 1 * 5 + index][0], area_list[ 2 * 5 + index][0], area_list[ 5 * 5 + index][0], 
                        area_list[16 * 5 + index][0], area_list[17 * 5 + index][0], area_list[18 * 5 + index][0], area_list[21 * 5 + index][0]
                    ]
        index = 1
        ireg_list = [
                        area_list[ 0 * 5 + index][0], area_list[ 1 * 5 + index][0], area_list[ 2 * 5 + index][0], area_list[ 5 * 5 + index][0], 
                        area_list[16 * 5 + index][0], area_list[17 * 5 + index][0], area_list[18 * 5 + index][0], area_list[21 * 5 + index][0]
                    ]
        index = 2
        wreg_list = [
                        area_list[ 0 * 5 + index][0], area_list[ 1 * 5 + index][0], area_list[ 2 * 5 + index][0], area_list[ 5 * 5 + index][0], 
                        area_list[16 * 5 + index][0], area_list[17 * 5 + index][0], area_list[18 * 5 + index][0], area_list[21 * 5 + index][0]
                    ]
        index = 3
        mul_list = [
                        area_list[ 0 * 5 + index][0], area_list[ 1 * 5 + index][0], area_list[ 2 * 5 + index][0], area_list[ 5 * 5 + index][0], 
                        area_list[16 * 5 + index][0], area_list[17 * 5 + index][0], area_list[18 * 5 + index][0], area_list[21 * 5 + index][0]
                    ]
        index = 4
        acc_list = [
                        area_list[ 0 * 5 + index][0], area_list[ 1 * 5 + index][0], area_list[ 2 * 5 + index][0], area_list[ 5 * 5 + index][0], 
                        area_list[16 * 5 + index][0], area_list[17 * 5 + index][0], area_list[18 * 5 + index][0], area_list[21 * 5 + index][0]
                    ]

        bot_list    = []
        bot1_list   = []
        bot2_list   = []
        top_list    = []

        for i in range(len(x_axis)-2):
            bot_list.append(ireg_list[i])
            bot1_list.append(bot_list[i] + wreg_list[i])
            bot2_list.append(bot1_list[i] + mul_list[i])
            top_list.append(bot2_list[i] + acc_list[i])
        
        if print_area:
            print("8-bit implementation:")
            print("SRAM area: ", sram_list[0])
            print("SA area (BP, BS, UR, UT): ", top_list[0:4])
            print("BS/BP SA area reduction:      ", 1 - top_list[1] / top_list[0])
            print("UR/BP SA area reduction:      ", 1 - top_list[2] / top_list[0])
            print("UT/BP SA area reduction:      ", 1 - top_list[3] / top_list[0])
            print("BS/BP on-chip area reduction: ", 1 - top_list[1] / (top_list[0] + sram_list[0]))
            print("UR/BP on-chip area reduction: ", 1 - top_list[2] / (top_list[0] + sram_list[0]))
            print("UT/BP on-chip area reduction: ", 1 - top_list[3] / (top_list[0] + sram_list[0]))
            print("UR/BS SA area reduction:      ", 1 - top_list[2] / top_list[1])
            print("UT/BS SA area reduction:      ", 1 - top_list[3] / top_list[1])
            print("UR/BS on-chip area reduction: ", 1 - top_list[2] / (top_list[1] + sram_list[0]))
            print("UT/BS on-chip area reduction: ", 1 - top_list[3] / (top_list[1] + sram_list[0]))

            print("16-bit implementation:")
            print("SRAM area: ", sram_list[4])
            print("SA area (BP, BS, UR, UT): ", top_list[4:8])
            print("BS/BP SA area reduction:      ", 1 - top_list[5] / top_list[4])
            print("UR/BP SA area reduction:      ", 1 - top_list[6] / top_list[4])
            print("UT/BP SA area reduction:      ", 1 - top_list[7] / top_list[4])
            print("BS/BP on-chip area reduction: ", 1 - top_list[5] / (top_list[4] + sram_list[4]))
            print("UR/BP on-chip area reduction: ", 1 - top_list[6] / (top_list[4] + sram_list[4]))
            print("UT/BP on-chip area reduction: ", 1 - top_list[7] / (top_list[4] + sram_list[4]))
            print("UR/BS SA area reduction:      ", 1 - top_list[6] / top_list[5])
            print("UT/BS SA area reduction:      ", 1 - top_list[7] / top_list[5])
            print("UR/BS on-chip area reduction: ", 1 - top_list[6] / (top_list[5] + sram_list[4]))
            print("UT/BS on-chip area reduction: ", 1 - top_list[7] / (top_list[5] + sram_list[4]))

        orc = "#7A81FF"
        sal = "#FF7F7F"
        lav = "#D783FF"
        gry_1 = "#666666"
        gry_2 = "#888888"
        gry_3 = "#AAAAAA"

        ax.bar(x_idx[0], sram_list[0], width, hatch = None, alpha=0.99, color=gry_1, label='SRAM')
        ax.bar(x_idx[5], sram_list[4], width, hatch = None, alpha=0.99, color=gry_1)
        ax.bar(np.concatenate((x_idx[1:5],x_idx[6:])), ireg_list, width, hatch = None, alpha=0.99, color=sal, label='IREG')
        ax.bar(np.concatenate((x_idx[1:5],x_idx[6:])), wreg_list, width, bottom=bot_list, hatch = None, alpha=0.99, color=orc, label='WREG')
        ax.bar(np.concatenate((x_idx[1:5],x_idx[6:])), mul_list,  width, bottom=bot1_list, hatch = None, alpha=0.99, color=lav, label='MUL')
        ax.bar(np.concatenate((x_idx[1:5],x_idx[6:])), acc_list,  width, bottom=bot2_list, hatch = None, alpha=0.99, color=gry_3, label='ACC')

        ax.set_ylabel('Area (mm^2)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis, rotation=45)
        if a == "eyeriss":
            ax.legend(ncol=2, frameon=True)
            bottom, top = plt.ylim()
            ax.set_ylim(bottom, 0.5)
            ax.text(0, 0.52, "{:.2f}".format(sram_list[0]), horizontalalignment="center")
            ax.text(5, 0.52, "{:.2f}".format(sram_list[4]), horizontalalignment="center")
            ax.text(6, 0.52, "({:.2f}".format(bot2_list[4])+",{:.2f})".format(top_list[4]), horizontalalignment="center")
        else:
            bottom, top = plt.ylim()
            ax.set_ylim(bottom, 300)
            ax.text(6, 312, "({:.2f}".format(bot2_list[4])+",{:.2f})".format(top_list[4]), horizontalalignment="center")
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Area_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Area fig saved!\n")


        # energy
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 2
        else:
            fig_h = 1.5
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        bg_color = "#D783FF"

        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 5

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx = 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bp_color)

        # 8b - spm - bs
        index = 1
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bs_color)

        # 8b - wospm - ur - 32c
        index = 10
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u6_color)

        # 8b - wospm - ur - 64c
        index = 11
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u7_color)

        # 8b - wospm - ur - 128c
        index = 12
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u8_color)

        ax.set_ylabel('SRAM-SA energy (uJ)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        bottom, top = plt.ylim()

        if a == "eyeriss":
            ax.set_ylim((bottom, top*50))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top/50], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        ax.axhline(y=0, color="k", linewidth = 0.1)
        
        plt.yscale("symlog", linthreshy=10000)
        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[:-1]
        else:
            locs = locs
        ax.set_yticks(locs)
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Energy_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Energy fig saved!\n")



        # power
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 2
        else:
            fig_h = 1.5
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        bg_color = "#D783FF"

        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 5

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx = 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bp_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bp_color)
        sram_d_list_bp_spm = []
        sram_dl_list_bp_spm = []
        for i in range(len(sram_d_list)):
            sram_d_list_bp_spm.append(sram_d_list[i])
            sram_dl_list_bp_spm.append(sram_d_list[i] + sram_l_list[i])

        # 8b - spm - bs
        index = 1
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=bs_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=bs_color)

        # 8b - wospm - ur - 32c
        index = 10
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u6_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u6_color)

        # 8b - wospm - ur - 64c
        index = 11
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u7_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u7_color)

        # 8b - wospm - ur - 128c
        index = 12
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        sram_d_neg_list = [-x for x in sram_d_list]
        sram_l_neg_list = [-x for x in sram_l_list]
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_d_list, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sarr_l_list, width, bottom=sarr_d_list, hatch = None, alpha=l_alpha, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_d_neg_list, width, hatch = None, alpha=0.99, color=u8_color)
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), sram_l_neg_list, width, bottom=sram_d_neg_list, hatch = None, alpha=l_alpha, color=u8_color)

        ax.set_ylabel('SRAM-SA Power (mW)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("linear")
        bottom, top = plt.ylim()

        if a == "eyeriss":
            ax.set_ylim((-300, 100))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, 50], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.legend(loc="upper center", ncol=3, frameon=True)
            ax.text(0-1.5*width, -284, "{:.2f}".format(sram_dl_list_bp_spm[0]), horizontalalignment="center")
            ax.text(1-1.5*width, -250, "({:.2f}".format(sram_d_list_bp_spm[1])+",{:.2f})".format(sram_dl_list_bp_spm[1]), horizontalalignment="center")
            ax.text(2-1.5*width, -284, "{:.2f}".format(sram_dl_list_bp_spm[2]), horizontalalignment="center")
    
            y_tick_list = [-200, -100, 0, 100]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
        else:
            ax.set_ylim((bottom, top))
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            
            y_tick_list = [-5000, 0, 5000]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
        ax.axhline(y=0, color="k", linewidth = 0.1)
        
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Power_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)
        print("Power fig saved!\n")



        # total energy with dram
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        bg_color = "#D783FF"

        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 5

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        total_energy_list_bp_spm = []
        onchip_energy_list_bp_spm = []
        for i in range(len(x_axis)):
            total_energy_list_bp_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_bp_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx = 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_bp_spm, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')

        # 8b - spm - bs
        index = 1
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        total_energy_list_bs_spm = []
        onchip_energy_list_bs_spm = []
        for i in range(len(x_axis)):
            total_energy_list_bs_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_bs_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_bs_spm, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')

        onchip_energy_r_list_bs_spm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_bs_spm.append(1-onchip_energy_list_bs_spm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_bs_spm = []
        for i in range(len(x_axis)):
            total_energy_r_list_bs_spm.append(1 - total_energy_list_bs_spm[i]/total_energy_list_bp_spm[i])

        # 8b - wospm - ur - 32c
        index = 10
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        total_energy_list_u6_wspm = []
        onchip_energy_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_u6_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_u6_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_u6_wspm, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')

        onchip_energy_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_u6_wspm.append(1-onchip_energy_list_u6_wspm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_u6_wspm.append(1 - total_energy_list_u6_wspm[i]/total_energy_list_bp_spm[i])

        # 8b - wospm - ur - 64c
        index = 11
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        total_energy_list_u7_wspm = []
        onchip_energy_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_u7_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_u7_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_u7_wspm, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')

        onchip_energy_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_u7_wspm.append(1-onchip_energy_list_u7_wspm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_u7_wspm.append(1 - total_energy_list_u7_wspm[i]/total_energy_list_bp_spm[i])

        # 8b - wospm - ur - 128c
        index = 12
        dram_d_list = energy_list[index * 5 + 0][:-1]
        sram_d_list = energy_list[index * 5 + 1][:-1]
        sram_l_list = energy_list[index * 5 + 2][:-1]
        sarr_d_list = energy_list[index * 5 + 3][:-1]
        sarr_l_list = energy_list[index * 5 + 4][:-1]
        total_energy_list_u8_wspm = []
        onchip_energy_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_energy_list_u8_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_energy_list_u8_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_energy_list_u8_wspm, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')

        onchip_energy_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            onchip_energy_r_list_u8_wspm.append(1-onchip_energy_list_u8_wspm[i]/onchip_energy_list_bp_spm[i])
        
        total_energy_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_energy_r_list_u8_wspm.append(1 - total_energy_list_u8_wspm[i]/total_energy_list_bp_spm[i])

        ax.set_ylabel('Total energy (uJ)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("log")

        _, top = plt.ylim()

        locs, labels = plt.yticks()
        if a == "eyeriss":
            locs = locs[1:]
        else:
            locs = locs[1:]
        ax.set_yticks(locs)
        
        bottom, _ = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        else:
            ax.set_ylim((bottom, top))
            bottom, top = plt.ylim()
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
        
        y_label_list = []
        for y in locs:
            if y != 0:
                y_label_list.append("{:1.0E}".format(abs(y)))
            else:
                y_label_list.append("0")
        ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Energy_total_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)

        if print_energy_onchip:
            print("On-chip energy reduction: ")
            print("binary parallel (baseline):", onchip_energy_list_bp_spm)
            print("binary serial             :", onchip_energy_r_list_bs_spm)
            print("unary 32c                 :", onchip_energy_r_list_u6_wspm)
            print("unary 64c                 :", onchip_energy_r_list_u7_wspm)
            print("unary 128c                :", onchip_energy_r_list_u8_wspm)
            print("min    reduction:", min(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            print("mean   reduction:", mean(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_energy_r_list_u6_wspm + onchip_energy_r_list_u7_wspm + onchip_energy_r_list_u8_wspm)*100, "%")
            
        if print_energy_total:
            print("Total energy reduction: ")
            print("binary parallel (baseline):", total_energy_list_bp_spm)
            print("binary serial             :", total_energy_r_list_bs_spm)
            print("unary 32c                 :", total_energy_r_list_u6_wspm)
            print("unary 64c                 :", total_energy_r_list_u7_wspm)
            print("unary 128c                :", total_energy_r_list_u8_wspm)
            print("min    reduction:", min(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            print("mean   reduction:", mean(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(total_energy_r_list_u6_wspm + total_energy_r_list_u7_wspm + total_energy_r_list_u8_wspm)*100, "%")

        print("Energy total fig saved!\n")


        # total power with dram
        my_dpi = 300
        if a == "eyeriss":
            fig_h = 1
        else:
            fig_h = 1
        fig_w = 3.3115

        bp_color = "#7A81FF"
        bs_color = "#FF7F7F"
        u6_color = "#666666"
        u7_color = "#888888"
        u8_color = "#AAAAAA"
        bg_color = "#D783FF"

        x_axis = ["Conv1", "Conv2", "Conv3", "Conv4", "Conv5", "FC6", "FC7", "FC8"]

        fig, ax = plt.subplots(figsize=(fig_w, fig_h))
        
        idx_tot = 5

        x_idx = np.arange(len(x_axis))

        width = 1 / 2**(math.ceil(math.log2(idx_tot)))

        iterval = width
        
        l_alpha = 0.8

        # 8b - spm - bp
        index = 0
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        total_power_list_bp_spm = []
        onchip_power_list_bp_spm = []
        for i in range(len(x_axis)):
            total_power_list_bp_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_bp_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx = 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_bp_spm, width, hatch = None, alpha=0.99, color=bp_color, label='Binary Parallel')


        # 8b - spm - bs
        index = 1
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        total_power_list_bs_spm = []
        onchip_power_list_bs_spm = []
        for i in range(len(x_axis)):
            total_power_list_bs_spm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_bs_spm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_bs_spm, width, hatch = None, alpha=0.99, color=bs_color, label='Binary Serial')

        onchip_power_r_list_bs_spm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_bs_spm.append(1-onchip_power_list_bs_spm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_bs_spm = []
        for i in range(len(x_axis)):
            total_power_r_list_bs_spm.append(1 - total_power_list_bs_spm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ur - 32c
        index = 10
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        total_power_list_u6_wspm = []
        onchip_power_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_power_list_u6_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_u6_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_u6_wspm, width, hatch = None, alpha=0.99, color=u6_color, label='Unary-32c')

        onchip_power_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_u6_wspm.append(1-onchip_power_list_u6_wspm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_u6_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_u6_wspm.append(1 - total_power_list_u6_wspm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ur - 64c
        index = 11
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        total_power_list_u7_wspm = []
        onchip_power_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_power_list_u7_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_u7_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_u7_wspm, width, hatch = None, alpha=0.99, color=u7_color, label='Unary-64c')

        onchip_power_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_u7_wspm.append(1-onchip_power_list_u7_wspm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_u7_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_u7_wspm.append(1 - total_power_list_u7_wspm[i]/total_power_list_bp_spm[i])

        # 8b - wospm - ur - 128c
        index = 12
        dram_d_list = power_list[index * 5 + 0][:-1]
        sram_d_list = power_list[index * 5 + 1][:-1]
        sram_l_list = power_list[index * 5 + 2][:-1]
        sarr_d_list = power_list[index * 5 + 3][:-1]
        sarr_l_list = power_list[index * 5 + 4][:-1]
        total_power_list_u8_wspm = []
        onchip_power_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_power_list_u8_wspm.append(dram_d_list[i] + sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
            onchip_power_list_u8_wspm.append(sram_d_list[i] + sram_l_list[i] + sarr_d_list[i] + sarr_l_list[i])
        idx += 1
        ax.bar(x_idx + iterval * (idx - idx_tot / 2), total_power_list_u8_wspm, width, hatch = None, alpha=0.99, color=u8_color, label='Unary-128c')

        onchip_power_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            onchip_power_r_list_u8_wspm.append(1-onchip_power_list_u8_wspm[i]/onchip_power_list_bp_spm[i])
        
        total_power_r_list_u8_wspm = []
        for i in range(len(x_axis)):
            total_power_r_list_u8_wspm.append(1 - total_power_list_u8_wspm[i]/total_power_list_bp_spm[i])


        ax.set_ylabel('Total power (mW)')
        ax.set_xticks(x_idx)
        ax.set_xticklabels(x_axis)
        plt.xlim(x_idx[0]-0.5, x_idx[-1]+0.5)
        plt.yscale("linear")

        bottom, top = plt.ylim()
        if a == "eyeriss":
            ax.set_ylim(bottom, 2500)
            for x in x_idx:
                ax.fill_betweenx([bottom, top], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            ax.text(0-1.5*width, 2600, "{:.2f}".format(total_power_list_bp_spm[0]), horizontalalignment="right")
            ax.text(0-0.5*width, 2600, "{:.2f}".format(total_power_list_bs_spm[0]), horizontalalignment="left")

            y_tick_list = [0, 1000, 2000]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)
        else:
            ax.set_ylim(bottom, top)
            for x in x_idx:
                ax.fill_betweenx([bottom, top+2000], x1=x, x2=x+0.5, alpha=0.2, color=bg_color, linewidth=0)
            y_tick_list = [0, 5000, 10000]
            ax.set_yticks(y_tick_list)
            y_label_list = []

            for y in y_tick_list:
                if y != 0:
                    y_label_list.append("{:1.0E}".format(abs(y)))
                else:
                    y_label_list.append("0")
            ax.set_yticklabels(y_label_list)

        ax.minorticks_off()
        fig.tight_layout()
        plt.savefig('./outputs_fig/' + technode + '/Power_total_' + a_cap + ".pdf", bbox_inches='tight', dpi=my_dpi, pad_inches=0.02)

        if print_power_onchip:
            print("On-chip power reduction: ")
            print("binary parallel (baseline):", onchip_power_list_bp_spm)
            print("binary serial             :", onchip_power_r_list_bs_spm)
            print("unary 32c                 :", onchip_power_r_list_u6_wspm)
            print("unary 64c                 :", onchip_power_r_list_u7_wspm)
            print("unary 128c                :", onchip_power_r_list_u8_wspm)
            print("min    reduction:", min(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")
            print("mean    reduction:", mean(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")
            print("max    reduction:", max(onchip_power_r_list_u6_wspm + onchip_power_r_list_u7_wspm + onchip_power_r_list_u8_wspm)*100, "%")

        if print_power_total:
            print("Total power reduction: ")
            print("binary parallel (baseline):", total_power_list_bp_spm)
            print("binary serial             :", total_power_r_list_bs_spm)
            print("unary 32c                 :", total_power_r_list_u6_wspm)
            print("unary 64c                 :", total_power_r_list_u7_wspm)
            print("unary 128c                :", total_power_r_list_u8_wspm)
            print("min    reduction:", min(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")
            print("mean   reduction:", mean(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")
            print("median reduction:", median(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")
            print("min    reduction:", max(total_power_r_list_u6_wspm + total_power_r_list_u7_wspm + total_power_r_list_u8_wspm)*100, "%")

        print("Power total fig saved!\n")
        

        print()


def prune(input_list):
    l = []

    for e in input_list:
        e = e.strip() # remove the leading and trailing characters, here space
        if e != '' and e != ' ':
            l.append(e)

    return l


def return_indexed_elems(input_csv=None, index=None):
    l = []

    csv_file = open(input_csv, "r")
    
    first = True
    for entry in csv_file:
        if first == True:
            first = False
            continue

        elems = entry.strip().split(',')
        elems = prune(elems)
        if len(elems) > 0:
            l.append(float(elems[index]))
    
    csv_file.close()

    return l


if __name__ == '__main__':
    plot_fig()
    # plot_fig(technode="45nm_rvt")
