import {
  Component,
  OnInit,
  Input,
  Output,
  ViewChild,
  EventEmitter,
} from '@angular/core';

import { Wallmount, Post } from '../../models/items.model';
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

  _totalWidthL: number;
  _totalWidthR: number;
  _globalWidth: number;
  _globalHeight: number;
  _leftMount: string;
  _rightMount: string;
  _glassType: string;

  @Input() set totalWidthL(val: number) {
    this._totalWidthL = val;
    if (this.leftWall) {
      this.leftWall.totalWidth = val;
      this.leftWall.autoCalculate();
      this.updatePackageList();
    }
  }

  @Input() set totalWidthR(val: number) {
    this._totalWidthR = val;
    if (this.rightWall) {
      this.rightWall.totalWidth = val;
      this.rightWall.autoCalculate();
      this.updatePackageList();
    }
  }

  @Input() set globalWidth(val: number) {
    this._globalWidth = val;
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

  @Input() set globalHeight(val: number) {
    this._globalHeight = val;
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

  @Input() set leftMount(val: string) {
    this._leftMount = val;
    if (this.leftWall?.items.length > 0) {
      this.leftWall.leftMount = val;
      this.updatePackageList();
    }
  }

  @Input() set rightMount(val: string) {
    this._rightMount = val;
    if (this.rightWall?.items.length > 0) {
      this.rightWall.rightMount = val;
      this.updatePackageList();
    } else if (this.leftWall?.items.length > 0) {
      this.leftWall.rightMount = val;
      this.updatePackageList();
    }
  }

  @Input() set glassType(val: string) {
    this._glassType = val;
    if (this.leftWall && this.rightWall) {
      this.leftWall.glassType = val;
      this.rightWall.glassType = val;
      this.updatePackageList();
    }
  }

  @Input() individualWidth: number;
  @Input() individualHeight: number;

  get leftWallRightMount(): string {
    return this.rightWall?.items.length > 0 ? 'post' : this._rightMount;
  }

  constructor() {}

  ngOnInit(): void {}

  addWallmount() {
    if (this.rightWall) {
      if (this.rightWall.items.length > 0) {
        // If the right wall is not empty, add wallmount there
        this.rightWall.addWallmount(this.individualHeight);
      } else {
        // If right wall is empty, try to add wallmount to left wall
        if (!this.leftWall.addWallmount(this.individualHeight))
          // If left wall is full, add to right wall
          this.rightWall.addWallmount(this.individualHeight);
      }
    } else if (this.leftWall) {
      this.leftWall.addWallmount(this.individualHeight);
    }
    this.updatePackageList();
  }

  addPost() {
    if (this.rightWall) {
      if (this.rightWall.items.length > 0) {
        // If the right wall is not empty, add post there
        this.rightWall.addPost(this.individualHeight);
      } else {
        // If right wall is empty, try to add post to left wall
        if (!this.leftWall.addPost(this.individualHeight))
          // If left wall is full, add to right wall
          this.rightWall.addPost(this.individualHeight);
      }
    } else if (this.leftWall) {
      this.leftWall.addPost(this.individualHeight);
    }
    this.updatePackageList();
  }

  addGlass(secondHeight = -1) {
    if (this.rightWall) {
      if (this.rightWall.items.length > 0) {
        // If the right wall is not empty, add glass there
        this.rightWall.addGlass(
          this.individualWidth,
          this.individualHeight,
          secondHeight,
        );
      } else {
        // If right wall is empty, try to add glass to left wall
        if (
          !this.leftWall.addGlass(
            this.individualWidth,
            this.individualHeight,
            secondHeight,
          )
        )
          // If left wall is full, add to right wall
          this.rightWall.addGlass(
            this.individualWidth,
            this.individualHeight,
            secondHeight,
          );
      }
    } else if (this.leftWall) {
      this.leftWall.addGlass(
        this.individualWidth,
        this.individualHeight,
        secondHeight,
      );
    }
    this.updatePackageList();
  }

  clear() {
    this.leftWall?.clear();
    this.rightWall?.clear();
    this.updatePackageList();
  }

  undo() {
    if (this.rightWall && this.rightWall.undo()) {
    } else if (this.leftWall) this.leftWall.undo();
    this.updatePackageList();
  }

  toggleWrap() {
    document.getElementById('container').classList.toggle('wrap');
  }

  _updatePackageList(map, items) {
    const glassType = '(' + this._glassType + ')';
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
}

const setDefault = (map, key, val) => {
  if (!(key in map)) map[key] = val;
  return map;
};
