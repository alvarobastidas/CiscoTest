from flask import Flask, render_template, request, jsonify


def selection(selected_list):
    selected = [list(item)[0] for item in selected_list]
    return selected


