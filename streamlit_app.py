import streamlit as st 
import os
import sys
import subprocess
import shlex
from datetime import datetime

def save(s: subprocess.CompletedProcess):
    if 'outputs' not in st.session_state:
        st.session_state['outputs'] = []
    st.session_state['outputs'].append({
            'returned_at': datetime.now(),
            'args': s.args,
            'stdout': str(s.stdout),
            'return_code': s.returncode,
            'stderr': str(s.stderr),
        })

def list_files(startpath):
    l = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        l.append('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            l.append('{}{}'.format(subindent, f))
            print('{}{}'.format(subindent, f))
    return '\n'.join(l)

st.title("🌐 Streamlit Shell 🌐")
with st.expander("diagnostic"):
    st.code(list_files(os.getcwd()))
    st.code(f"sys.path: {sys.path}")
    st.code(f"sys.argv: {sys.argv}" )
    st.code(f"sys.executable: {sys.executable}")
    st.code(f"sys.flags: {sys.flags}")

cmd_txt = st.text_input("command input: ", help='This will call a simple subprocess.run(<input>). The input is best effort parsed by shlex')
if cmd_txt and cmd_txt != "":
    try:
        s = subprocess.run(shlex.split(cmd_txt), capture_output=True)
        save(s)
        if s.returncode!= 0: 
            st.warning(f'non-zero return: {s.returncode}', icon="⚠️")
        st.code(s.stdout.decode())
    except Exception as inst:
        st.error(inst)


if 'outputs' in st.session_state:
    st.caption('hint: double click on long outputs')
    st.dataframe(st.session_state['outputs'])
