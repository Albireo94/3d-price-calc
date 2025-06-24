import * as THREE from '/static/libs/three.module.js';
import { OrbitControls } from '/static/libs/OrbitControls.js';
import { STLLoader } from '/static/libs/STLLoader.js';

export function renderSTLInContainer(arrayBuffer, containerId) {
  const container = document.getElementById(containerId);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableZoom = false;
  controls.enablePan = false;

  const light = new THREE.HemisphereLight(0xffffff, 0x444444);
  scene.add(light);

  const loader = new STLLoader();
  const geometry = loader.parse(arrayBuffer);
  const material = new THREE.MeshStandardMaterial({ color: 0x007bff });
  const mesh = new THREE.Mesh(geometry, material);
  scene.add(mesh);

  // Center and scale
  const box = new THREE.Box3().setFromObject(mesh);
  const size = new THREE.Vector3();
  box.getSize(size);
  const maxDim = Math.max(size.x, size.y, size.z);
  const center = box.getCenter(new THREE.Vector3());
  mesh.position.sub(center);  // Center model
  camera.position.set(maxDim, maxDim, maxDim);
  camera.lookAt(0, 0, 0);

  function animate() {
    requestAnimationFrame(animate);
    mesh.rotation.y += 0.01;
    renderer.render(scene, camera);
  }

  animate();
}
