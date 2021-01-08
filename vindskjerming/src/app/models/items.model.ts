import * as Config from '../config.json';

export class Item {
  width: number;
  height: number;
  color: string;
  secondHeight?: number;
  _isLast = false;

  set isLast(val: boolean) {
    this._isLast = val;
  }

  get isPolygon(): boolean {
    return false;
  }

  get weight(): number {
    return 0;
  }
}

export class Wallmount extends Item {
  width = Config['wallmount']['width'];
  color = 'grey';

  constructor(height: number) {
    super();
    this.height = +height.toFixed(2);
  }

  get weight(): number {
    const multiplier = 0.1;
    const packaging = 50;
    return this.height * multiplier + packaging;
  }
}

export class Post extends Item {
  lastWidth = Config['post']['lastWidth'];
  color = 'black';

  constructor(height: number) {
    super();
    this.isLast = true;
    this.height = +height.toFixed(2);
  }

  set isLast(val: boolean) {
    this._isLast = val;
    this.width = val ? Config['post']['lastWidth'] : Config['post']['width'];
  }

  get weight(): number {
    const multiplier = 0.1568;
    const postMountWeight = 54;
    const packaging = 100;
    return this.height * multiplier + postMountWeight + packaging;
  }
}

export class Glass extends Item {
  constructor(
    glassType: string,
    width: number,
    height: number,
    secondHeight?: number,
  ) {
    super();
    this.width = +width.toFixed(2);
    this.height = +height.toFixed(2);
    this.secondHeight = secondHeight ? +secondHeight.toFixed(2) : this.height;
    this.glassType = glassType;
  }

  set glassType(val: string) {
    this.color = val === 'klart' ? 'blue' : 'red';
  }

  get weight(): number {
    const area =
      this.width * this.height -
      (this.width * (this.height - this.secondHeight)) / 2;
    const multiplier = 0.618;
    const packaging = 200;
    return area * multiplier + packaging;
  }

  get isPolygon(): boolean {
    return this.height !== this.secondHeight;
  }
}
