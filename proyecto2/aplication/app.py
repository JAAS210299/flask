from flask import Flask, abort, render_template, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from aplication import config
from aplication.config import os
from aplication.forms import formArticulo, formSINO, formCategoria
from werkzeug.utils import secure_filename
from aplication.models import Articulos, Categorias, db


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config.from_object(config)

db.init_app(app)

@app.route('/')
@app.route('/categoria/<id>')
def inicio(id='0'):
    categoria=Categorias.query.get(id)
    if id=='0':
        articulos=Articulos.query.all()
    else:
        articulos=Articulos.query.filter_by(CategoriaId=id)
    categorias=Categorias.query.all()
    return render_template("inicio.html", articulos=articulos,categorias=categorias,categoria=categoria)

@app.route('/categorias')
def categorias():
    categorias=Categorias.query.all()
    return render_template("categorias.html", categorias=categorias)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Página no encontrada..."), 404

@app.route('/articulos/new', methods=["get", "post"])
def articulos_new():
    form=formArticulo()
    categorias=[(c.id, c.nombre) for c in Categorias.query.all()[0:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        try:
            f = form.photo.data
            nombre_fichero=secure_filename(f.filename)
            f.save(app.root_path+"/static/img/"+nombre_fichero)
        except:
            nombre_fichero=""
        art=Articulos()
        form.populate_obj(art)
        art.image=nombre_fichero
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("inicio"))
    else:
        return render_template("articulos_new.html", form=form)
    
@app.route('/categorias/new', methods=["get","post"])
def categorias_new():
    form=formCategoria(request.form)
    if form.validate_on_submit():
        cat=Categorias(nombre=form.nombre.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for("categorias"))
    else:
        return render_template("categorias_new.html", form=form)
    
@app.route('/articulos/<id>/edit', methods=["get", "post"])
def articulos_edit(id):

    art=Articulos.query.get(id)
    if art is None:
        abort(404)
    form=formArticulo(obj=art)
    categorias=[(c.id, c.nombre) for c in Categorias.query.all()[0:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        if form.photo.data: #Borramos la imagen anterior si hemos subido una nueva
            if art.image:
                os.remove(app.root_path+"/static/img/"+art.image)
            try:
                f = form.photo.data
                nombre_fichero=secure_filename(f.filename)
                f.save(app.root_path+"/static/img/"+nombre_fichero)
            except:
                nombre_fichero=""
        else:
            nombre_fichero=art.image
        form.populate_obj(art)
        art.image=nombre_fichero
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("articulos_new.html", form=form)

@app.route('/articulos/<id>/delete', methods=["get", "post"])
def articulos_delete(id):
    art=Articulos.query.get(id)
    if art is None:
        abort(404)
    form=formSINO() 
    if form.validate_on_submit():
        if form.si.data:
            if art.image!="":
                os.remove(app.root_path+"/static/img/"+art.image)
            db.session.delete(art)
            db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("articulos_delete.html",form=form,art=art)
