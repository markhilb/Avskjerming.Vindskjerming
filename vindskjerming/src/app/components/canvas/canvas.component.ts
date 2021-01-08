import {
  Component,
  OnInit,
  Input,
  Output,
  ViewChild,
  EventEmitter,
} from '@angular/core';

import { Item, Wallmount, Post } from '../../models/items.model';
import { WallComponent } from './wall/wall.component';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss'],
})
export class CanvasComponent implements OnInit {
  @ViewChild('leftWall') leftWall: WallComponent;
  @ViewChild('rightWall') rightWall: WallComponent;

  @Output() packageListChanged = new EventEmitter<any>();

  @Input() totalWidthL: number;
  @Input() totalWidthR: number;
  @Input() globalWidth: number;
  @Input() globalHeight: number;
  @Input() individualWidth: number;
  @Input() individualHeight: number;
  @Input() glassType: string;
  @Input() leftMount: string;
  @Input() rightMount: string;

  constructor() {}

  ngOnInit(): void {}

  get leftWallRightMount(): string {
    return this.rightWall?.items.length > 0 ? 'post' : this.rightMount;
  }

  setTotalWidthL(val: number) {
    this.totalWidthL = val;
    if (this.leftWall) {
      this.leftWall.totalWidth = val;
      this.leftWall.autoCalculate();
      this.updatePackageList();
    }
  }

  setTotalWidthR(val: number) {
    this.totalWidthR = val;
    if (this.rightWall) {
      this.rightWall.totalWidth = val;
      this.rightWall.autoCalculate();
      this.updatePackageList();
    }
  }

  setGlobalWidth(val: number) {
    this.globalWidth = val;
    if (val >= 10) {
      if (this.leftWall) {
        if (this.leftWall) {
          this.rightWall.globalWidth = val;
          this.rightWall.autoCalculate();
        }
        this.leftWall.globalWidth = val;
        this.leftWall.autoCalculate();
      }
    } else {
      this.leftWall?.clear();
      this.rightWall?.clear();
    }
    this.updatePackageList();
  }

  setGlobalHeight(val: number) {
    this.globalHeight = val;
    if (val >= 10) {
      if (this.leftWall) {
        if (this.rightWall) {
          this.rightWall.globalHeight = val;
          this.rightWall.autoCalculate();
        }
        this.leftWall.globalHeight = val;
        this.leftWall.autoCalculate();
      }
    } else {
      this.leftWall?.clear();
      this.rightWall?.clear();
    }
    this.updatePackageList();
  }

  setGlassType(val: string) {
    this.glassType = val;
    if (this.leftWall && this.rightWall) {
      this.leftWall.glassType = val;
      this.rightWall.glassType = val;
      this.updatePackageList();
    }
  }

  setLeftMount(val: string) {
    this.leftMount = val;
    if (this.leftWall?.items.length > 0) {
      this.leftWall.leftMount = val;
      this.updatePackageList();
    }
  }

  setRightMount(val: string) {
    this.rightMount = val;
    if (this.rightWall?.items.length > 0) {
      this.rightWall.rightMount = val;
      this.updatePackageList();
    } else if (this.leftWall?.items.length > 0) {
      this.leftWall.rightMount = val;
      this.updatePackageList();
    }
  }

  addWallmount() {
    if (
      this.leftWall?.addWallmount(this.individualHeight) ||
      this.rightWall?.addWallmount(this.individualHeight)
    )
      this.updatePackageList();
  }

  addPost() {
    if (
      this.leftWall?.addPost(this.individualHeight) ||
      this.rightWall?.addPost(this.individualHeight)
    )
      this.updatePackageList();
  }

  addGlass(secondHeight = -1) {
    if (
      this.leftWall?.addGlass(
        this.individualWidth,
        this.individualHeight,
        secondHeight,
      ) ||
      this.rightWall?.addGlass(
        this.individualWidth,
        this.individualHeight,
        secondHeight,
      )
    )
      this.updatePackageList();
  }

  clear() {
    this.leftWall?.clear();
    this.rightWall?.clear();
    this.updatePackageList();
  }

  undo() {
    if (this.rightWall?.undo() || this.leftWall?.undo())
      this.updatePackageList();
  }

  toggleWrap() {
    document.getElementById('container').classList.toggle('wrap');
  }

  _updatePackageList(map, items) {
    const glassType = '(' + this.glassType + ')';
    let key: string;
    let size: string;
    items.forEach((item) => {
      size = `${+item.height.toFixed(2)}`;
      if (item instanceof Wallmount) {
        key = 'Veggskinne';
      } else if (item instanceof Post) {
        key = 'Stolpe';
      } else {
        if (item.height !== item.secondHeight) {
          key = 'Skrå glass ' + glassType;
          size = `${+item.width.toFixed(2)}x${+item.height.toFixed(
            2,
          )}x${+item.secondHeight.toFixed(2)}`;
        } else {
          key = 'Glass ' + glassType;
          size = `${+item.width.toFixed(2)}x${+item.height.toFixed(2)}`;
        }
      }
      setDefault(setDefault(map, key, {})[key], size, 0)[size] += 1;
      map['weight'] += item.weight;
    });
  }

  updatePackageList() {
    const map = { weight: 0 };
    if (this.leftWall) this._updatePackageList(map, this.leftWall.items);
    if (this.rightWall) this._updatePackageList(map, this.rightWall.items);

    const res = { weight: map.weight, list: [] };
    delete map.weight;
    Object.entries(map).map(([key, val]) => {
      Object.entries(val).map(([size, num]) => {
        res.list.push([key, size, num]);
        key = '';
      });
    });
    this.packageListChanged.emit(res);
  }

  _itemsAsJson = (items: Item[]) =>
    items.map((item) => {
      if (item instanceof Wallmount) return ['Wallmount', item.height];
      else if (item instanceof Post) return ['Post', item.height];
      return ['Glass', `${item.width}x${item.height}x${item.secondHeight}`];
    });

  itemsAsJson = () => [
    this._itemsAsJson(this.leftWall.items),
    this._itemsAsJson(this.rightWall.items),
  ];

  loadItems(items, totalWidthL, totalWidthR) {
    this.leftWall.loadItems(items[0], totalWidthL);
    this.rightWall.loadItems(items[1], totalWidthR);
    this.updatePackageList();
  }
}

const setDefault = (map, key, val) => {
  if (!(key in map)) map[key] = val;
  return map;
};
