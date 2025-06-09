// components/RoutineInput.jsx

import { useState } from "react";
import { generateFullRoutine } from "../../services/oBCalls";

function RoutineInput() {
  const [inputType, setInputType] = useState("text");
  const [productName, setProductName] = useState("");
  const [productList, setProductList] = useState([]);
  const [routine, setRoutine] = useState([]);
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAddProduct = () => {
    if (productName.trim() === "") return;
    setProductList((prev) => [...prev, { product_name: productName }]);
    setProductName("");
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
        // Aquí llamarías a tu OCR backend si lo tuvieras
        // Por ahora solo mostramos la imagen
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGenerateRoutine = async () => {
    if (productList.length === 0) return;
    setLoading(true);
    const result = await generateFullRoutine(productList);
    if (result) setRoutine(result);
    setLoading(false);
  };

  const handleRemoveProduct = (indexToRemove) => {
    setProductList((prev) => prev.filter((_, i) => i !== indexToRemove));
  };

  return (
    <div>
      <h2>Agregar Productos</h2>

      <div>
        <label>
          <input
            type="radio"
            name="inputType"
            value="text"
            checked={inputType === "text"}
            onChange={() => setInputType("text")}
          />
          Ingresar por nombre
        </label>

        <label>
          <input
            type="radio"
            name="inputType"
            value="image"
            checked={inputType === "image"}
            onChange={() => setInputType("image")}
          />
          Subir imagen del producto
        </label>
      </div>

      {inputType === "text" ? (
        <div>
          <input
            type="text"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            placeholder="Nombre del producto"
          />
          <button onClick={handleAddProduct}>Agregar</button>
        </div>
      ) : (
        <div>
          <input type="file" accept="image/*" onChange={handleImageUpload} />
          {imagePreview && <img src={imagePreview} alt="preview" width="150" />}
        </div>
      )}

      <div>
        <h3>Lista de productos</h3>
        <ul>
          {productList.map((p, i) => (
            <li key={i}>
              {p.product_name}
              <button onClick={() => handleRemoveProduct(i)}>❌</button>
            </li>
          ))}
        </ul>
      </div>

      <button onClick={handleGenerateRoutine}>Generar rutina</button>
      {loading && <p>Generando rutina...</p>}

      {routine.length > 0 && (
        <div>
          <h3>Tu rutina ordenada:</h3>
          <ol>
            {routine.map((item, index) => (
              <li key={index}>
                <strong>{item.product_name}</strong> ({item.step})
                {item.ingredients_text && (
                  <p>
                    <em>Ingredientes:</em> {item.ingredients_text}
                  </p>
                )}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default RoutineInput;
