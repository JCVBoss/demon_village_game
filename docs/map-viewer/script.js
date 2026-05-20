class MapViewer {
    constructor() {
        this.canvas = document.getElementById('map-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.currentMap = null;
        this.zoom = 1;
        this.tileSize = 32;
        
        this.maps = {
            village: null,
            forest: null,
            world: null
        };
        
        this.init();
    }
    
    async init() {
        await this.loadMaps();
        this.setupEventListeners();
        this.selectMap('village');
    }
    
    async loadMaps() {
        try {
            const [village, forest, world] = await Promise.all([
                fetch('village_config.json').then(r => r.json()),
                fetch('forest_config.json').then(r => r.json()),
                fetch('world_config.json').then(r => r.json())
            ]);
            
            this.maps.village = village;
            this.maps.forest = forest;
            this.maps.world = world;
        } catch (e) {
            console.error('加载地图失败:', e);
        }
    }
    
    setupEventListeners() {
        document.getElementById('map-select').addEventListener('change', (e) => {
            this.selectMap(e.target.value);
        });
        
        document.getElementById('zoom-in').addEventListener('click', () => {
            this.adjustZoom(0.2);
        });
        
        document.getElementById('zoom-out').addEventListener('click', () => {
            this.adjustZoom(-0.2);
        });
        
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }
    
    selectMap(mapType) {
        this.currentMap = this.maps[mapType];
        if (!this.currentMap) return;
        
        const mapData = this.currentMap.map || this.currentMap.world;
        if (mapData) {
            let width, height;
            if (mapData.size) {
                width = mapData.size.width * this.tileSize;
                height = mapData.size.height * this.tileSize;
            } else {
                width = 600;
                height = 400;
            }
            
            this.canvas.width = width;
            this.canvas.height = height;
        }
        
        this.render();
        this.updateInfoPanel();
    }
    
    adjustZoom(delta) {
        this.zoom = Math.max(0.5, Math.min(3, this.zoom + delta));
        document.getElementById('zoom-level').textContent = `${Math.round(this.zoom * 100)}%`;
        this.render();
    }
    
    render() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (!this.currentMap) return;
        
        const mapType = document.getElementById('map-select').value;
        
        switch(mapType) {
            case 'village':
                this.renderVillage();
                break;
            case 'forest':
                this.renderForest();
                break;
            case 'world':
                this.renderWorld();
                break;
        }
    }
    
    renderVillage() {
        const map = this.maps.village;
        
        this.ctx.fillStyle = '#4a7c59';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (map.roads) {
            map.roads.forEach(road => {
                this.drawRoad(road);
            });
        }
        
        if (map.buildings) {
            map.buildings.forEach(building => {
                this.drawBuilding(building);
            });
        }
        
        if (map.npcSpawnPoints) {
            map.npcSpawnPoints.forEach(npc => {
                this.drawNPC(npc);
            });
        }
        
        if (map.eventTriggers) {
            map.eventTriggers.forEach(event => {
                this.drawEventTrigger(event);
            });
        }
        
        if (map.decorations) {
            if (map.decorations.trees) {
                map.decorations.trees.forEach(tree => {
                    this.drawTree(tree);
                });
            }
        }
    }
    
    renderForest() {
        const map = this.maps.forest;
        
        this.ctx.fillStyle = '#2d5a27';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (map.zones) {
            map.zones.forEach(zone => {
                this.drawZone(zone);
            });
        }
        
        if (map.paths) {
            map.paths.forEach(path => {
                this.drawPath(path);
            });
        }
        
        if (map.features) {
            Object.keys(map.features).forEach(key => {
                this.drawFeature(key, map.features[key]);
            });
        }
        
        if (map.resources) {
            if (map.resources.herbs && map.resources.herbs.locations) {
                map.resources.herbs.locations.forEach(loc => {
                    this.drawResource(loc, '#6bcb77', '🌿');
                });
            }
        }
    }
    
    renderWorld() {
        const map = this.maps.world;
        
        this.ctx.fillStyle = '#1a2a1a';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        if (map.regions) {
            map.regions.forEach((region, index) => {
                this.drawRegion(region, index);
            });
        }
    }
    
    drawRoad(road) {
        const fromX = road.from.x * this.tileSize;
        const fromY = road.from.y * this.tileSize;
        const toX = road.to.x * this.tileSize;
        const toY = road.to.y * this.tileSize;
        const width = road.width * this.tileSize;
        
        this.ctx.fillStyle = road.type === 'stone' ? '#8b7355' : '#a0826d';
        
        if (road.from.x === road.to.x) {
            this.ctx.fillRect(fromX - width/2, Math.min(fromY, toY), width, Math.abs(toY - fromY) + this.tileSize);
        } else {
            this.ctx.fillRect(Math.min(fromX, toX), fromY - width/2, Math.abs(toX - fromX) + this.tileSize, width);
        }
    }
    
    drawBuilding(building) {
        const x = building.position.x * this.tileSize;
        const y = building.position.y * this.tileSize;
        const w = building.size.width * this.tileSize;
        const h = building.size.height * this.tileSize;
        
        this.ctx.fillStyle = building.enterable ? '#8b4513' : '#5a3010';
        this.ctx.fillRect(x, y, w, h);
        
        this.ctx.strokeStyle = '#3d2817';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x, y, w, h);
        
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '10px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(building.name, x + w/2, y + h/2 + 4);
    }
    
    drawNPC(npc) {
        const x = npc.position.x * this.tileSize + this.tileSize/2;
        const y = npc.position.y * this.tileSize + this.tileSize/2;
        
        this.ctx.beginPath();
        this.ctx.arc(x, y, 10, 0, Math.PI * 2);
        this.ctx.fillStyle = '#ff6b6b';
        this.ctx.fill();
        this.ctx.strokeStyle = '#fff';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
        
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '8px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(npc.npc, x, y - 15);
    }
    
    drawEventTrigger(event) {
        const x = event.position.x * this.tileSize + this.tileSize/2;
        const y = event.position.y * this.tileSize + this.tileSize/2;
        const r = event.radius * this.tileSize;
        
        this.ctx.beginPath();
        this.ctx.arc(x, y, r, 0, Math.PI * 2);
        this.ctx.fillStyle = 'rgba(255, 217, 61, 0.3)';
        this.ctx.fill();
        this.ctx.strokeStyle = '#ffd93d';
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
        
        this.ctx.fillStyle = '#ffd93d';
        this.ctx.font = '10px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('⚡', x, y + 4);
    }
    
    drawTree(tree) {
        const x = tree.position.x * this.tileSize;
        const y = tree.position.y * this.tileSize;
        
        this.ctx.fillStyle = '#228b22';
        this.ctx.beginPath();
        this.ctx.arc(x + this.tileSize/2, y + this.tileSize/2, 8, 0, Math.PI * 2);
        this.ctx.fill();
    }
    
    drawZone(zone) {
        const x = zone.position.x * this.tileSize;
        const y = zone.position.y * this.tileSize;
        const w = zone.size.width * this.tileSize;
        const h = zone.size.height * this.tileSize;
        
        this.ctx.fillStyle = zone.safety ? 'rgba(107, 203, 119, 0.3)' : 'rgba(255, 68, 68, 0.3)';
        this.ctx.fillRect(x, y, w, h);
        
        this.ctx.strokeStyle = zone.safety ? '#6bcb77' : '#ff4444';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x, y, w, h);
        
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '12px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(zone.name, x + w/2, y + 15);
    }
    
    drawPath(path) {
        this.ctx.strokeStyle = path.type === 'dirt' ? '#8b7355' : '#4a7c59';
        this.ctx.lineWidth = path.width * this.tileSize;
        this.ctx.lineCap = 'round';
        
        if (path.waypoints && path.waypoints.length > 1) {
            this.ctx.beginPath();
            this.ctx.moveTo(path.waypoints[0].x * this.tileSize, path.waypoints[0].y * this.tileSize);
            for (let i = 1; i < path.waypoints.length; i++) {
                this.ctx.lineTo(path.waypoints[i].x * this.tileSize, path.waypoints[i].y * this.tileSize);
            }
            this.ctx.stroke();
        } else {
            this.ctx.beginPath();
            this.ctx.moveTo(path.from.x * this.tileSize, path.from.y * this.tileSize);
            this.ctx.lineTo(path.to.x * this.tileSize, path.to.y * this.tileSize);
            this.ctx.stroke();
        }
    }
    
    drawFeature(key, feature) {
        if (!feature.position) return;
        
        const x = feature.position.x * this.tileSize;
        const y = feature.position.y * this.tileSize;
        
        this.ctx.fillStyle = '#ffd93d';
        this.ctx.font = '16px sans-serif';
        this.ctx.textAlign = 'center';
        
        let emoji = '📍';
        if (key === 'mushroom_circle') emoji = '🍄';
        if (key === 'ancient_trees') emoji = '🌳';
        if (key === 'firefly_clearing') emoji = '✨';
        if (key === 'abandoned_camp') emoji = '⛺';
        
        this.ctx.fillText(emoji, x + this.tileSize/2, y + this.tileSize/2 + 6);
    }
    
    drawResource(loc, color, emoji) {
        const x = loc.x * this.tileSize;
        const y = loc.y * this.tileSize;
        
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '12px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(emoji, x + this.tileSize/2, y + this.tileSize/2 + 4);
    }
    
    drawRegion(region, index) {
        const baseX = this.canvas.width / 2;
        const baseY = this.canvas.height / 2;
        
        const regionPositions = {
            twilight_village: { x: 0, y: 0 },
            mist_forest: { x: 0, y: 80 },
            demon_castle: { x: 0, y: -120 },
            kingdom: { x: 0, y: 180 },
            northern_wasteland: { x: 0, y: -60 }
        };
        
        const pos = regionPositions[region.id] || { x: 0, y: 0 };
        
        const colors = {
            village: '#4a90e2',
            forest: '#4a7c59',
            castle: '#8b0000',
            kingdom: '#808080',
            wasteland: '#4a0000'
        };
        
        const x = baseX + pos.x;
        const y = baseY + pos.y;
        
        this.ctx.beginPath();
        this.ctx.arc(x, y, 30, 0, Math.PI * 2);
        this.ctx.fillStyle = colors[region.type] || '#666';
        this.ctx.fill();
        this.ctx.strokeStyle = region.explorable ? '#fff' : '#333';
        this.ctx.lineWidth = 3;
        this.ctx.stroke();
        
        this.ctx.fillStyle = '#fff';
        this.ctx.font = '12px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(region.name, x, y + 50);
        
        if (!region.explorable) {
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.beginPath();
            this.ctx.arc(x, y, 28, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.fillStyle = '#666';
            this.ctx.font = '14px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText('🔒', x, y + 5);
        }
    }
    
    handleMouseMove(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const tileX = Math.floor(x / this.tileSize);
        const tileY = Math.floor(y / this.tileSize);
        
        console.log(`位置: (${tileX}, ${tileY})`);
    }
    
    handleClick(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const tileX = Math.floor(x / this.tileSize);
        const tileY = Math.floor(y / this.tileSize);
        
        this.showTileInfo(tileX, tileY);
    }
    
    showTileInfo(tileX, tileY) {
        const info = { x: tileX, y: tileY };
        
        if (this.currentMap && this.currentMap.buildings) {
            for (const building of this.currentMap.buildings) {
                if (tileX >= building.position.x && tileX < building.position.x + building.size.width &&
                    tileY >= building.position.y && tileY < building.position.y + building.size.height) {
                    info.building = building;
                    break;
                }
            }
        }
        
        console.log('瓦片信息:', info);
    }
    
    updateInfoPanel() {
        const titleEl = document.getElementById('info-title');
        const contentEl = document.getElementById('info-content');
        
        if (!this.currentMap) {
            contentEl.innerHTML = '<p>加载中...</p>';
            return;
        }
        
        const mapType = document.getElementById('map-select').value;
        let html = '';
        
        if (mapType === 'village') {
            const map = this.maps.village;
            titleEl.textContent = map.map.name;
            
            html = `
                <div class="info-item">
                    <span class="info-label">地图ID:</span>
                    <span class="info-value">${map.map.id}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">尺寸:</span>
                    <span class="info-value">${map.map.size.width} x ${map.map.size.height} 瓦片</span>
                </div>
                <div class="info-item">
                    <span class="info-label">建筑数量:</span>
                    <span class="info-value">${map.buildings ? map.buildings.length : 0}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">NPC数量:</span>
                    <span class="info-value">${map.npcSpawnPoints ? map.npcSpawnPoints.length : 0}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">事件点数量:</span>
                    <span class="info-value">${map.eventTriggers ? map.eventTriggers.length : 0}</span>
                </div>
            `;
        } else if (mapType === 'forest') {
            const map = this.maps.forest;
            titleEl.textContent = map.map.name;
            
            html = `
                <div class="info-item">
                    <span class="info-label">地图ID:</span>
                    <span class="info-value">${map.map.id}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">尺寸:</span>
                    <span class="info-value">${map.map.size.width} x ${map.map.size.height} 瓦片</span>
                </div>
                <div class="info-item">
                    <span class="info-label">区域数量:</span>
                    <span class="info-value">${map.zones ? map.zones.length : 0}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">描述:</span>
                    <span class="info-value">${map.map.description}</span>
                </div>
            `;
        } else if (mapType === 'world') {
            const map = this.maps.world;
            titleEl.textContent = map.world.name;
            
            html = `
                <div class="info-item">
                    <span class="info-label">纪元:</span>
                    <span class="info-value">${map.world.era}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">区域总数:</span>
                    <span class="info-value">${map.world.totalRegions}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">已探索区域:</span>
                    <span class="info-value">${map.world.exploredRegions}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">描述:</span>
                    <span class="info-value">${map.world.description}</span>
                </div>
            `;
        }
        
        contentEl.innerHTML = html;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new MapViewer();
});
