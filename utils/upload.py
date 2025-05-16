import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static\uploads'
ALLOWED_EXTENSIONS = {'png'}